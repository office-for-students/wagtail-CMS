(function () {
    "use strict";

    const GA_ID = "UA-147556197-1";
    const ACCEPTED = "discoverUniAnalyticsCookies";
    const DECLINED = "discoverUniAnalyticsCookiesDeclined";
    const ONE_YEAR = 60 * 60 * 24 * 365;

    /* ---------- cookies ---------- */

    function getCookie(name) {
        // Exact match on the name. The old includes() check treated
        // "discoverUniAnalyticsCookiesDeclined" as also matching "discoverUniAnalyticsCookies".
        const match = document.cookie.split("; ").find((c) => c.split("=")[0] === name);
        return match ? match.slice(name.length + 1) : null;
    }

    function setCookie(name, value) {
        const secure = location.protocol === "https:" ? "; Secure" : "";
        document.cookie = `${name}=${value}; Max-Age=${ONE_YEAR}; Path=/; SameSite=Lax${secure}`;
    }

    function deleteCookie(name) {
        // GA writes to the parent domain, so clear every possible domain.
        const parts = location.hostname.split(".");
        const domains = [""];
        for (let i = 0; i < parts.length - 1; i++) {
            domains.push("; Domain=." + parts.slice(i).join("."));
        }
        domains.forEach((d) => {
            document.cookie = `${name}=; Max-Age=0; Path=/${d}`;
        });
    }

    /* ---------- Google Analytics ---------- */

    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };

    function gaAlreadyOnPage() {
        return !!document.querySelector('script[src*="googletagmanager.com/gtag/js"]');
    }

    function startAnalytics() {
        window["ga-disable-" + GA_ID] = false;
        window.gtag("consent", "update", { analytics_storage: "granted" });

        // On later page loads the server may already render the tag – don't add a second copy.
        if (gaAlreadyOnPage()) return;

        const s = document.createElement("script");
        s.async = true;
        s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
        document.head.appendChild(s);

        window.gtag("js", new Date());
        window.gtag("config", GA_ID); // records this page view, so no reload is needed
    }

    function stopAnalytics() {
        window["ga-disable-" + GA_ID] = true;
        window.gtag("consent", "update", { analytics_storage: "denied" });
        document.cookie.split("; ").forEach((c) => {
            const name = c.split("=")[0];
            if (name === "_ga" || name === "_gid" || name.startsWith("_ga_") || name.startsWith("_gat")) {
                deleteCookie(name);
            }
        });
    }

    /* ---------- the manager ---------- */

    class CookieManagement {
        constructor() {
            this.banner = document.getElementById("cookie-banner");
            this.settings = document.getElementById("cookie-settings");
            this.form = document.getElementById("settings_form");
            this.noRadio = document.getElementById("no_decline");
            this.status = document.getElementById("cookie-status");

            if (!this.banner || !this.settings) return;

            this.setListeners(); // always wire up, so people can change their mind later

            const state = this.currentState();
            if (state === "accepted") startAnalytics();
            this.syncForm(state);

            if (this.isCookiePage()) {
                // On /cookies/, show the Yes/No settings rather than hiding everything.
                this.hide(this.banner);
                this.show(this.settings);
            } else if (state) {
                this.hideAll();
            } else {
                this.show(this.banner);
                this.hide(this.settings);
            }
        }

        currentState() {
            if (getCookie(ACCEPTED)) return "accepted";
            if (getCookie(DECLINED)) return "declined";
            return null;
        }

        isCookiePage() {
            // The old indexOf("cookies") check matched any URL containing the word.
            return /^\/cookies\/?$/.test(location.pathname);
        }

        setListeners() {
            const acceptBtn = document.getElementById("cookie_accept");
            const settingsBtn = document.getElementById("cookie_settings");
            const rejectBtn = document.getElementById("cookie_reject");

            acceptBtn?.addEventListener("click", (ev) => {
                ev.preventDefault();
                this.saveChoice(true);
            });

            rejectBtn?.addEventListener("click", (ev) => {
                ev.preventDefault();
                this.saveChoice(false);
            });

            settingsBtn?.addEventListener("click", (ev) => {
                ev.preventDefault();
                this.openSettings();
            });

            // The Yes/No form and the accept button now go through the same saveChoice().
            this.form?.addEventListener("submit", (ev) => {
                ev.preventDefault();
                const choice = this.selectedChoice();
                if (choice === null) {
                    // The old code treated "nothing selected" as accepting.
                    this.announce("Choose yes or no before saving your cookie settings.");
                    this.form.querySelector('input[type="radio"]')?.focus();
                    return;
                }
                this.saveChoice(choice);
            });

            document.querySelectorAll("[data-cookie-open]").forEach((link) => {
                link.addEventListener("click", (ev) => {
                    ev.preventDefault();
                    this.openSettings();
                });
            });
        }

        selectedChoice() {
            const checked = this.form?.querySelector('input[type="radio"]:checked');
            if (!checked) return null;
            return checked !== this.noRadio; // true = accept analytics
        }

        syncForm(state) {
            if (!this.form || !state) return;
            const radios = this.form.querySelectorAll('input[type="radio"]');
            radios.forEach((r) => {
                r.checked = state === "declined" ? r === this.noRadio : r !== this.noRadio;
            });
        }

        saveChoice(accepted) {
            if (accepted) {
                setCookie(ACCEPTED, "accepted");
                deleteCookie(DECLINED); // previously both cookies could exist at once
                startAnalytics();
            } else {
                setCookie(DECLINED, "declined");
                deleteCookie(ACCEPTED);
                stopAnalytics();
            }
            this.syncForm(accepted ? "accepted" : "declined");

            if (this.isCookiePage()) {
                // Leave the settings visible on the cookies page; just confirm.
                this.hide(this.banner);
            } else {
                this.hideAll();
            }

            this.announce(accepted
                ? "You've accepted analytics cookies. You can change this at any time on the cookies page."
                : "You've rejected analytics cookies. You can change this at any time on the cookies page.");
            // No window.location.reload()
        }

        openSettings() {
            this.hide(this.banner);
            this.show(this.settings);
            this.syncForm(this.currentState());
            const first = this.settings.querySelector('input[type="radio"]:checked, input[type="radio"]');
            first?.focus();
        }

        hideAll() {
            const hadFocus = this.banner.contains(document.activeElement)
                || this.settings.contains(document.activeElement);
            this.hide(this.banner);
            this.hide(this.settings);
            if (hadFocus) {
                // Don't leave keyboard users focused on a hidden element.
                const main = document.querySelector("main") || document.body;
                if (!main.hasAttribute("tabindex")) main.setAttribute("tabindex", "-1");
                main.focus({ preventScroll: true });
            }
        }

        show(el) { el.style.display = "block"; el.hidden = false; }
        hide(el) { el.style.display = "none"; el.hidden = true; }

        announce(message) {
            if (!this.status) return;
            this.status.textContent = "";
            setTimeout(() => { this.status.textContent = message; }, 50);
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", () => new CookieManagement());
    } else {
        new CookieManagement();
    }
})();