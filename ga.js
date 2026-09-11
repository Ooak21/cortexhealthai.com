// GA4 for cortexhealthai.com.
//
// One file rather than the snippet pasted into every page, so the
// measurement ID lives in exactly one place. Loaded from /ga.js with defer
// on the home page, the Vitality OS case study, and both checkout pages.
//
// Property: Innovative Blockchain Solutions > cortexhealthai.com
// Stream: Main (15760640894)
//
// Pages report conversions through window.cxTrack(name, params), which is
// a thin wrapper over gtag so a page never has to know whether GA loaded.
(function () {
  var ID = 'G-2SV6CF0HTB';

  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  gtag('js', new Date());
  gtag('config', ID);

  window.cxTrack = function (name, params) {
    try { gtag('event', name, params || {}); } catch (e) {}
  };

  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + ID;
  document.head.appendChild(s);
})();
