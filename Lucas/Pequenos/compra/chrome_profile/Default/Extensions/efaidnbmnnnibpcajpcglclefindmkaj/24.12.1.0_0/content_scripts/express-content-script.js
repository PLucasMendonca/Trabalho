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
function createDomAnchor(e,t=2147483646){if(document.querySelector(`#${e}`))return document.querySelector(`#${e}`);const r=document.createElement("div");return r.id=e,r.style.position="fixed",r.style.zIndex=`${t}`,r.style.width="100%",r.style.height="100%",r.style.top="0",r.style.colorScheme="light",r.style.backgroundColor="rgba(0, 0, 0, 0.5)",r.style.display="block",document.body.style.overflow="hidden",r}function openExpressEditorInFrame(){const e=createDomAnchor("expressAcrobatExtension"),t=chrome.runtime.getURL("browser/js/express.html"),r=document.createElement("iframe");r.setAttribute("src",t),r.setAttribute("id","expressAcrobatExtensionIframe"),r.setAttribute("allowfullscreen","true"),r.setAttribute("allow","clipboard-read; clipboard-write;"),r.style.width="100%",r.style.height="100%",r.style.border="none",r.style.overflow="hidden",e.appendChild(r),document.body.insertBefore(e,document.body.childNodes[0])}openExpressEditorInFrame();