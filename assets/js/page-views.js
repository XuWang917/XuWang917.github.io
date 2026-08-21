(function () {
  var container = document.querySelector("[data-page-view-counter]");
  if (!container) return;

  var value = container.querySelector(".page__footer-counter-value");
  var callbackName =
    "BusuanziHomepageCallback_" + Math.floor(Math.random() * 1000000000);
  var request = document.createElement("script");
  var timeout;

  function render(count) {
    value.textContent = count;
    container.hidden = false;
    container.setAttribute("aria-label", count + " page views");
    container.setAttribute("title", count + " page views");
  }

  function cleanup() {
    if (timeout) window.clearTimeout(timeout);
    if (request.parentNode) request.parentNode.removeChild(request);
    try {
      delete window[callbackName];
    } catch (error) {
    window[callbackName] = undefined;
    }
  }

  if (window.location.hostname === "localhost") return;
  if (window.location.hostname === "127.0.0.1") return;

  window[callbackName] = function (data) {
    var count = Number(data && data.site_pv);
    if (!Number.isFinite(count)) {
      cleanup();
      return;
    }

    render(count);
    cleanup();
  };

  request.async = true;
  request.referrerPolicy = "no-referrer-when-downgrade";
  request.src =
    "https://busuanzi.ibruce.info/busuanzi?jsonpCallback=" +
    encodeURIComponent(callbackName);
  request.onerror = cleanup;

  document.head.appendChild(request);
  timeout = window.setTimeout(cleanup, 8000);
})();
