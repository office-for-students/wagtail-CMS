(function () {
    class CookieManagement {
        constructor(banner, setting) {
            this.banner = banner;
            this.settings = setting;

            if (window.location.href.indexOf("cookies") > -1) {
                this.hideCookieBanners()
            } else if (
                !document.cookie.includes("discoverUniAnalyticsCookiesDeclined")
                && !document.cookie.includes("discoverUniAnalyticsCookies")
            ) {
                this.showCookieBanner()
                this.setListeners()
            } else {
                this.hideCookieBanners()
            }

        }

        setListeners() {
            let settings_btn = document.getElementById("cookie_settings")
            let accept_btn = document.getElementById("cookie_accept")

            settings_btn.addEventListener("click", (ev) => {
                this.hideCookieBanners()
                this.showSettingControls()
            })

            accept_btn.addEventListener("click", (ev) => {
                this.acceptAllCookies();
                this.hideCookieBanners();
            })

            const settings_form = document.getElementById("settings_form");
            settings_form.addEventListener("submit", (event) => {
                event.preventDefault()
                const declined = this.isDeclined()
                if (declined) {
                    this.declinedCookies()
                    this.hideCookieBanners()
                } else {
                    this.acceptAllCookies()
                    this.hideCookieBanners()
                }
            });
        }

        hideCookieBanners() {
            this.banner.style.display = "none";
            this.settings.style.display = "none";
        }

        showCookieBanner() {
            this.banner.style.display = "block";
        }

        showSettingControls() {
            this.settings.style.display = "block";
        }

        declinedCookies() {
            let CookieDate = new Date;
            CookieDate.setFullYear(CookieDate.getFullYear() +1);
            document.cookie = "discoverUniAnalyticsCookiesDeclined=declined; expires=" + CookieDate.toUTCString() + ";path=/";
            window.location.reload()
        }

        acceptAllCookies() {
            let CookieDate = new Date;
            CookieDate.setFullYear(CookieDate.getFullYear() +1);
            document.cookie = "discoverUniAnalyticsCookies=accepted; expires=" + CookieDate.toUTCString() + ";path=/";
            window.location.reload()
        }

        isDeclined() {
            const decline = document.getElementById("no_decline")
            return decline.checked
        }
    }

    let cookieManager = new CookieManagement(
        document.getElementById("cookie-banner"),
        document.getElementById("cookie-settings")
    )


})();

