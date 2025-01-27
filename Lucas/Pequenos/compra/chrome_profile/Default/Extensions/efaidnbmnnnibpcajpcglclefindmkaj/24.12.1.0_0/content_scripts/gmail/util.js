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
import state from"./state.js";const ACROBAT_ICON_CLASS="acrobat-icon",ACROBAT_LISTENER_ADDED="acrobat-listener-added",ACROBAT_CONTENT_SCRIPT_DISCONNECT_START="acrobatContentScriptDisconnectStart",LIST_VIEW="LIST_VIEW",DRIVE_USERCONTENT_URL="drive.usercontent.google.com",DRIVE_PDF_URL_PATTERN=`https://${DRIVE_USERCONTENT_URL}/download?id=_id&authuser=_authuser`,createAcrobatIconElement=()=>{const e=document.createElement("img");return e.setAttribute("src",state?.iconURL),e.setAttribute("class","acrobat-icon"),e},getElementBasedOnSelector=(e,t,r)=>{if(e){const n=state?.gmailConfig?.selectors,i=n&&n[r]&&n[r][t];for(let t=0;t<i?.length;t++){let r=e.querySelector(i[t]);if(r)return r}}return null},getClosestElementBasedOnSelector=(e,t,r)=>{if(e){const n=state?.gmailConfig?.selectors,i=n&&n[r]&&n[r][t];for(let t=0;t<i?.length;t++){let r=e.closest(i[t]);if(r)return r}}return null},getArrayElementBasedOnSelector=(e,t,r)=>{if(e){const n=state?.gmailConfig?.selectors,i=n&&n[r]&&n[r][t];for(let t=0;t<i?.length;t++)if(e?.querySelector(i[t])){const r=e?.querySelectorAll(i[t]);if(r&&r.length>0)return r}}return null},getFileDetailsElementInNativeViewer=()=>getElementBasedOnSelector(document,"lightBoxViewerFileDetails","nativeViewer"),isOrphanContentScript=()=>!chrome?.runtime?.id,createURLForAttachment=(e,t,r)=>{let n=e?.replace("disp=safe","disp=inline");return t&&(n=n+"&acrobatPromotionSource="+t),state?.viewerURLPrefix&&(n=`${state.viewerURLPrefix}?pdfurl=${encodeURIComponent(n)}`,r&&(n=n+"&pdffilename="+encodeURIComponent(r))),n},getUserId=()=>{const e=window.location?.pathname?.split("/");return e?.length>3?e[3]:"0"},updateDrivePDFUrl=e=>{const t=extractFileIdFromDriveUrl(e);return t?formDrivePDFUrl(t):(sendAnalytics([["DCBrowserExt:Gmail:ISDAParsingFailed:EmptyDriveFileId"]]),"")},formDrivePDFUrl=e=>DRIVE_PDF_URL_PATTERN.replace("_id",e).replace("_authuser",getUserId()),isDriveFileDirectDownloadLink=e=>e?.includes(DRIVE_USERCONTENT_URL),isDriveLinkAttachmentTouchPointEnabled=()=>state?.gmailConfig?.enableDriveLinkAttachmentPromptInGmail,extractFileIdFromDriveUrl=e=>e?e.split("/")[5]||new URL(e).searchParams.get("id"):"";export{ACROBAT_CONTENT_SCRIPT_DISCONNECT_START,ACROBAT_LISTENER_ADDED,LIST_VIEW,getFileDetailsElementInNativeViewer,getArrayElementBasedOnSelector,getElementBasedOnSelector,getClosestElementBasedOnSelector,createAcrobatIconElement,isOrphanContentScript,createURLForAttachment,getUserId,isDriveFileDirectDownloadLink,isDriveLinkAttachmentTouchPointEnabled,updateDrivePDFUrl};