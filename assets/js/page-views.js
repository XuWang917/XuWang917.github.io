(function () {
  var container = document.querySelector("[data-page-view-counter]");
  if (!container) return;

  var value = container.querySelector(".page__footer-counter-value");
  if (!value) return;
  var hostname = window.location.hostname;
  var cacheKey = "xuwang917-homepage-page-views-v2";
  var visitorKey = "xuwang917-homepage-visitor";
  var apiUrl =
    "https://xuwang917-homepage-counter.pmpm351613.chatgpt.site/api/views";
  var attempts = 0;

  function render(count) {
    value.textContent = count;
    container.hidden = false;
    container.setAttribute("aria-label", count + " page views");
    container.setAttribute("title", count + " page views");
  }

  function readCachedCount() {
    try {
      var cached = window.localStorage.getItem(cacheKey);
      var count = cached === null ? null : Number(cached);
      return Number.isSafeInteger(count) && count >= 0 ? count : null;
    } catch (error) {
      return null;
    }
  }

  function cacheCount(count) {
    try {
      window.localStorage.setItem(cacheKey, String(count));
    } catch (error) {
      // The live count still renders when storage is unavailable.
    }
  }

  function getVisitorId() {
    try {
      var visitorId = window.localStorage.getItem(visitorKey);
      if (!visitorId || !/^[a-f0-9-]{36}$/i.test(visitorId)) {
        visitorId = window.crypto.randomUUID();
        window.localStorage.setItem(visitorKey, visitorId);
      }
      return visitorId;
    } catch (error) {
      // The server can deduplicate requests when browser storage is blocked.
      return null;
    }
  }

  function requestJson(options) {
    var controller = new AbortController();
    var timeout = window.setTimeout(function () {
      controller.abort();
    }, 6000);

    return window
      .fetch(apiUrl, {
        method: options.method,
        headers: options.headers,
        body: options.body,
        cache: "no-store",
        credentials: "omit",
        signal: controller.signal,
      })
      .then(function (response) {
        if (!response.ok) throw new Error("Page view request failed");
        return response.json();
      })
      .finally(function () {
        window.clearTimeout(timeout);
      });
  }

  function loadCount() {
    attempts += 1;

    requestJson({
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ visitorId: getVisitorId() }),
    })
      .catch(function () {
        return requestJson({ method: "GET" });
      })
      .then(function (data) {
        var count = data && data.views;
        if (!Number.isSafeInteger(count) || count < 0) {
          throw new Error("Invalid page view count");
        }

        cacheCount(count);
        render(count);
      })
      .catch(function () {
        if (attempts < 3) {
          window.setTimeout(loadCount, attempts * 1800);
        }
      });
  }

  if (hostname !== "xuwang917.github.io") return;

  var cachedCount = readCachedCount();
  if (cachedCount !== null) render(cachedCount);
  loadCount();
})();
