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
const sendAnalytics=t=>{try{chrome.runtime.sendMessage({main_op:"analytics",analytics:t})}catch(t){}},formatDateForMonthlyAnalyticsEvent=t=>t instanceof Date?`${t.getUTCFullYear()}${(t.getUTCMonth()+1).toString().padStart(2,"0")}`:"",eventsSent=new Set,sendAnalyticsOnce=t=>{eventsSent?.has(t)||(eventsSent.add(t),sendAnalyticsEvent([t]))},sendAnalyticsOncePerMonth=async t=>{if(t)try{const n=await chrome.storage.local.get([t]),e=new Date,a=formatDateForMonthlyAnalyticsEvent(e),s=n?.[t]?.lastSentYearMonth;if(!s||a>s){sendAnalytics([t]);const n={lastSentYearMonth:a};chrome.storage.local.set({[t]:n})}}catch(t){}};export{sendAnalytics,sendAnalyticsOnce,sendAnalyticsOncePerMonth};