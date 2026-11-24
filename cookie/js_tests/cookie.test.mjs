// Behaviour tests for cookie/static/cookie.js.
// Run with: node --test cookie/js_tests/ (also run from CMS/test_google_analytics.py via pytest).
// Uses only Node built-ins: the real cookie.js runs inside a vm context against a tiny fake DOM.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import vm from "node:vm";

const SOURCE = readFileSync(new URL("../static/cookie.js", import.meta.url), "utf8");
const GA4_ID = "G-9XTF7DN7MG";
const ACCEPTED = "discoverUniAnalyticsCookies";
const DECLINED = "discoverUniAnalyticsCookiesDeclined";
const GTAG_SRC = "googletagmanager.com/gtag/js";

/* ---------- minimal fake DOM ---------- */

class FakeElement {
    constructor(doc, tag, attrs = {}) {
        this.ownerDocument = doc;
        this.tagName = tag.toUpperCase();
        this.attributes = { ...attrs };
        this.children = [];
        this.parent = null;
        this.listeners = {};
        this.style = {};
        this.hidden = false;
        this.checked = false;
        this.async = false;
        this.textContent = "";
    }

    get id() { return this.attributes.id || ""; }
    get src() { return this.attributes.src || ""; }
    set src(value) { this.attributes.src = value; }

    getAttribute(name) { return name in this.attributes ? this.attributes[name] : null; }
    setAttribute(name, value) { this.attributes[name] = String(value); }
    hasAttribute(name) { return name in this.attributes; }

    appendChild(child) {
        child.parent = this;
        this.children.push(child);
        return child;
    }

    append(...children) {
        children.forEach((c) => this.appendChild(c));
        return this;
    }

    addEventListener(type, fn) { (this.listeners[type] ||= []).push(fn); }

    dispatch(type) {
        const ev = { type, defaultPrevented: false, preventDefault() { this.defaultPrevented = true; } };
        (this.listeners[type] || []).forEach((fn) => fn(ev));
        return ev;
    }

    click() { return this.dispatch("click"); }
    focus() { this.ownerDocument.activeElement = this; }
    contains(el) { return el === this || this.children.some((c) => c.contains(el)); }

    descendants() { return this.children.flatMap((c) => [c, ...c.descendants()]); }
    querySelectorAll(selector) { return this.descendants().filter((el) => matches(el, selector)); }
    querySelector(selector) { return this.querySelectorAll(selector)[0] || null; }
}

// Supports the selector subset cookie.js uses: tag, [attr], [attr="v"], [attr*="v"], :checked, and comma lists.
function matches(el, selector) {
    return selector.split(",").some((part) => {
        const m = part.trim().match(/^([a-z]+)?((?:\[[^\]]+\])*)(:checked)?$/i);
        if (!m) throw new Error(`Unsupported selector in fake DOM: ${part}`);
        const [, tag, attrs, checked] = m;
        if (tag && el.tagName !== tag.toUpperCase()) return false;
        if (checked && !el.checked) return false;
        for (const [, name, op, value] of attrs.matchAll(/\[([\w-]+)(?:(\*?=)"([^"]*)")?\]/g)) {
            const actual = el.getAttribute(name);
            if (actual === null) return false;
            if (op === "=" && actual !== value) return false;
            if (op === "*=" && !actual.includes(value)) return false;
        }
        return true;
    });
}

function createCookieJar(initial) {
    const jar = new Map(Object.entries(initial));
    return {
        jar,
        get() { return [...jar].map(([k, v]) => `${k}=${v}`).join("; "); },
        set(raw) {
            const [pair, ...attrs] = raw.split(";").map((s) => s.trim());
            const eq = pair.indexOf("=");
            const name = pair.slice(0, eq);
            const value = pair.slice(eq + 1);
            if (attrs.some((a) => /^max-age=0$/i.test(a))) jar.delete(name);
            else jar.set(name, value);
        },
    };
}

/**
 * Builds a page resembling base.html + cookie-banner.html and runs cookie.js against it.
 * gaIdAttr: undefined -> no data-ga-id attribute; otherwise its value.
 */
function loadPage({ cookies = {}, gaIdAttr = GA4_ID, banner = true, pathname = "/", extraHeadScripts = [] } = {}) {
    const doc = { activeElement: null, readyState: "interactive" };
    const el = (tag, attrs) => new FakeElement(doc, tag, attrs);
    const root = el("html");
    const head = el("head");
    const body = el("body");
    const main = el("main");
    root.append(head, body);
    body.appendChild(main);

    const cookieScriptAttrs = { src: "/static/cookie.js?1", defer: "" };
    if (gaIdAttr !== undefined) cookieScriptAttrs["data-ga-id"] = gaIdAttr;
    head.appendChild(el("script", cookieScriptAttrs));
    extraHeadScripts.forEach((src) => head.appendChild(el("script", { src })));

    let elements = {};
    if (banner) {
        const bannerEl = el("article", { id: "cookie-banner" });
        const accept = el("button", { id: "cookie_accept" });
        const settingsBtn = el("button", { id: "cookie_settings" });
        bannerEl.append(settingsBtn, accept);

        const settings = el("article", { id: "cookie-settings" });
        const form = el("form", { id: "settings_form" });
        const yes = el("input", { type: "radio", id: "yes_accept", name: "extra_cookies", value: "YES" });
        yes.checked = true;
        const no = el("input", { type: "radio", id: "no_decline", name: "extra_cookies", value: "NO" });
        const status = el("p", { id: "cookie-status" });
        form.append(yes, no, status);
        settings.appendChild(form);
        main.append(bannerEl, settings);
        elements = { banner: bannerEl, accept, settingsBtn, settings, form, yes, no, status };
    }

    const cookieJar = createCookieJar(cookies);
    const document = {
        get cookie() { return cookieJar.get(); },
        set cookie(v) { cookieJar.set(v); },
        get readyState() { return doc.readyState; },
        get activeElement() { return doc.activeElement; },
        head,
        body,
        createElement: (tag) => el(tag),
        getElementById: (id) => root.descendants().find((e) => e.id === id) || null,
        querySelector: (s) => root.querySelector(s),
        querySelectorAll: (s) => root.querySelectorAll(s),
        addEventListener() {},
    };

    const context = {
        document,
        location: { protocol: "https:", hostname: "discoveruni.gov.uk", pathname },
        setTimeout: (fn) => fn(),
    };
    context.window = context;
    vm.createContext(context);
    vm.runInContext(SOURCE, context, { filename: "cookie.js" });

    return { win: context, document, head, cookieJar: cookieJar.jar, ...elements };
}

// Array.from here builds arrays in this realm, so deepStrictEqual doesn't trip over vm-context prototypes.
const gtagCalls = (win) => Array.from(win.dataLayer, (entry) => Array.from(entry));
const configCalls = (win) => gtagCalls(win).filter(([cmd]) => cmd === "config");
const gtagScripts = (head) => head.children.filter((s) => s.tagName === "SCRIPT" && s.src.includes(GTAG_SRC));
const consentUpdates = (win) => gtagCalls(win).filter(([cmd, type]) => cmd === "consent" && type === "update");

function assertAnalyticsEnabled(page, id = GA4_ID) {
    const scripts = gtagScripts(page.head);
    assert.equal(scripts.length, 1, "exactly one gtag.js script should be on the page");
    assert.equal(scripts[0].src, `https://www.${GTAG_SRC}?id=${id}`);
    assert.equal(scripts[0].async, true);
    assert.deepEqual(configCalls(page.win).map(([, cfgId]) => cfgId), [id], "one page_view config for the GA4 ID");
    assert.ok(gtagCalls(page.win).some(([cmd]) => cmd === "js"), "gtag('js', date) must be sent");
    assert.equal(consentUpdates(page.win).at(-1)[2].analytics_storage, "granted");
    assert.equal(page.win[`ga-disable-${id}`], false);
}

function assertAnalyticsNotLoaded(page) {
    assert.equal(gtagScripts(page.head).length, 0, "gtag.js must not be loaded without consent");
    assert.equal(configCalls(page.win).length, 0, "no GA config/page_view without consent");
}

/* ---------- tests ---------- */

test("before any choice: consent defaults to denied, GA is not loaded and the banner is shown", () => {
    const page = loadPage();
    const [first] = gtagCalls(page.win);
    assert.deepEqual(first.slice(0, 2), ["consent", "default"]);
    assert.equal(first[2].analytics_storage, "denied");
    assert.equal(first[2].ad_storage, "denied");
    assertAnalyticsNotLoaded(page);
    assert.equal(page.banner.style.display, "block");
});

test("accepting via the banner loads GA4 with the configured ID and records the page view", () => {
    const page = loadPage();
    const ev = page.accept.click();

    assert.equal(ev.defaultPrevented, true);
    assert.equal(page.cookieJar.get(ACCEPTED), "accepted");
    assert.equal(page.cookieJar.has(DECLINED), false);
    assertAnalyticsEnabled(page);
    assert.equal(page.banner.style.display, "none");
    assert.equal(page.settings.style.display, "none");
});

test("consent default is queued before the consent grant and config", () => {
    const page = loadPage();
    page.accept.click();
    const cmds = gtagCalls(page.win).map(([cmd, arg]) => `${cmd}:${typeof arg === "string" ? arg : "date"}`);
    const idx = (c) => cmds.indexOf(c);
    assert.ok(idx("consent:default") < idx("consent:update"));
    assert.ok(idx("consent:update") < idx(`config:${GA4_ID}`));
    assert.ok(idx("js:date") < idx(`config:${GA4_ID}`));
});

test("returning visitor who accepted gets GA on page load", () => {
    const page = loadPage({ cookies: { [ACCEPTED]: "accepted" } });
    assertAnalyticsEnabled(page);
    assert.equal(page.banner.style.display, "none");
});

test("returning visitor who accepted gets GA even on pages without the cookie banner", () => {
    const page = loadPage({ cookies: { [ACCEPTED]: "accepted" }, banner: false });
    assertAnalyticsEnabled(page);
});

test("saving 'yes' in the settings form enables GA", () => {
    const page = loadPage();
    page.settingsBtn.click();
    page.yes.checked = true;
    page.no.checked = false;
    page.form.dispatch("submit");
    assert.equal(page.cookieJar.get(ACCEPTED), "accepted");
    assertAnalyticsEnabled(page);
});

test("saving 'no' in the settings form keeps GA off", () => {
    const page = loadPage();
    page.yes.checked = false;
    page.no.checked = true;
    page.form.dispatch("submit");
    assert.equal(page.cookieJar.get(DECLINED), "declined");
    assert.equal(page.cookieJar.has(ACCEPTED), false);
    assertAnalyticsNotLoaded(page);
    assert.equal(page.win[`ga-disable-${GA4_ID}`], true);
});

test("submitting the settings form with nothing selected does not enable GA", () => {
    const page = loadPage();
    page.yes.checked = false;
    page.no.checked = false;
    page.form.dispatch("submit");
    assert.equal(page.cookieJar.has(ACCEPTED), false);
    assertAnalyticsNotLoaded(page);
});

test("returning visitor who declined does not get GA (declined cookie name is not mistaken for accepted)", () => {
    const page = loadPage({ cookies: { [DECLINED]: "declined" } });
    assertAnalyticsNotLoaded(page);
});

test("changing from accepted to declined revokes consent and removes GA cookies", () => {
    const page = loadPage({
        cookies: { [ACCEPTED]: "accepted", _ga: "GA1.1.123", "_ga_9XTF7DN7MG": "GS1.1.1", _gid: "GA1.2.3" },
        pathname: "/cookies/",
    });
    assertAnalyticsEnabled(page);

    page.yes.checked = false;
    page.no.checked = true;
    page.form.dispatch("submit");

    assert.equal(consentUpdates(page.win).at(-1)[2].analytics_storage, "denied");
    assert.equal(page.win[`ga-disable-${GA4_ID}`], true);
    for (const name of ["_ga", "_ga_9XTF7DN7MG", "_gid", ACCEPTED]) {
        assert.equal(page.cookieJar.has(name), false, `${name} should be deleted`);
    }
    assert.equal(page.cookieJar.get(DECLINED), "declined");
});

test("accepting repeatedly does not inject gtag.js or send config more than once", () => {
    const page = loadPage();
    page.accept.click();
    page.accept.click();
    page.form.dispatch("submit");
    assertAnalyticsEnabled(page);
});

test("an existing gtag.js tag for the same ID is reused rather than duplicated", () => {
    const page = loadPage({
        cookies: { [ACCEPTED]: "accepted" },
        extraHeadScripts: [`https://www.${GTAG_SRC}?id=${GA4_ID}`],
    });
    assert.equal(gtagScripts(page.head).length, 1);
    assert.deepEqual(configCalls(page.win).map(([, id]) => id), [GA4_ID]);
});

test("a stale Universal Analytics tag on the page does not stop the GA4 tag loading", () => {
    const page = loadPage({
        cookies: { [ACCEPTED]: "accepted" },
        extraHeadScripts: [`https://www.${GTAG_SRC}?id=UA-147556197-1`],
    });
    assert.ok(gtagScripts(page.head).some((s) => s.src.endsWith(`id=${GA4_ID}`)));
});

test("the measurement ID from data-ga-id (Django settings) is used", () => {
    const page = loadPage({ gaIdAttr: "G-TEST123" });
    page.accept.click();
    assertAnalyticsEnabled(page, "G-TEST123");
});

test("data-ga-id is trimmed and normalised to upper case", () => {
    const page = loadPage({ gaIdAttr: "  g-test123 " });
    page.accept.click();
    assertAnalyticsEnabled(page, "G-TEST123");
});

test("falls back to the default GA4 ID when no data-ga-id attribute is present", () => {
    const page = loadPage({ gaIdAttr: undefined });
    page.accept.click();
    assertAnalyticsEnabled(page, GA4_ID);
});

for (const bad of ["", "UA-147556197-1", "G-", "G-abc\"><script>", "javascript:alert(1)"]) {
    test(`an empty or invalid data-ga-id (${JSON.stringify(bad)}) disables GA even after consent`, () => {
        const page = loadPage({ gaIdAttr: bad });
        page.accept.click();
        assert.equal(page.cookieJar.get(ACCEPTED), "accepted");
        assertAnalyticsNotLoaded(page);
    });
}

test("no Universal Analytics ID is ever sent to gtag", () => {
    const page = loadPage();
    page.accept.click();
    assert.ok(!JSON.stringify(gtagCalls(page.win)).includes("UA-"));
});
