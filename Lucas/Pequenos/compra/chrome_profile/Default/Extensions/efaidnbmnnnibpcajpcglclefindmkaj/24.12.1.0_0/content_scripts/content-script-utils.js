/*************************************************************************
* ADOBE CONFIDENTIAL
* ___________________
*
*  Copyright 2015 Adobe Systems Incorporated
*  All Rights Reserved.
*
* NOTICE:  All information contained herein is, and remains
* the property of Adobe Systems Incorporated and its suppliers,
* if any.  The intellectual and technical concepts contained
* herein are proprietary to Adobe Systems Incorporated and its
* suppliers and are protected by all applicable intellectual property laws,
* including trade secret and or copyright laws.
* Dissemination of this information or reproduction of this material
* is strictly forbidden unless prior written permission is obtained
* from Adobe Systems Incorporated.
**************************************************************************/
function isGoogleQuery(e){if(!e)return!1;try{const t=new URL(e);if(t.host.startsWith("www.google.")||t.host.startsWith("www.bing."))return!0}catch(e){return!1}return!1}function isSupportedBrowserVersion(){const e=navigator.userAgent.match(/Chrome\/([0-9]+)/);return!(e&&e.length>=2)||+e[1]>=SETTINGS.SUPPORTED_VERSION}function checkForThirdPartyCookiesStatus(e){const t=document.createElement("iframe");t.id="third-party-cookies-checker",t.style.display="none",t.src=chrome.runtime.getURL("browser/js/check-cookies.html");const r=(o,n,s)=>{"thirdPartyCookiesChecked"===o.content_op&&(t.remove(),chrome.runtime.onMessage.removeListener(r),e&&e(o.status))};chrome.runtime.onMessage.addListener(r),document.documentElement.appendChild(t)}