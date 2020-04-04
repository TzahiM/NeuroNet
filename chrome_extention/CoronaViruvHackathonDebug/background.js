// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
// Tzahi Manistersky mailto:tzahimanmobile@gmail.com +972(52)2947775
// Use under public liscense of https://github.com/TzahiM/NeuroNet
// Specially contribiuted for corona virus hackathon. Dedicated for turn ideas into projects and results

// Called when the user clicks on the browser action.
chrome.browserAction.onClicked.addListener(function(tab) {
	
//	var message = 'http://www.neuronetlabs.org';						 //the destination server
	var message = 'http://127.0.0.1:8000';						 //the destination server
	message    += '/CoronaVirusHackathon/coplay/extention_add_with_url/';//destination inner url
	message    += '?parent_url=' + tab.url; 							 //add current browser url  - should use first
	message    += '&parent_url_text=' + tab.title;						 //Add webpage name
	message    += '&ver=20.04.03.1';									 //add version number
	

	chrome.tabs.update(tab.id, { url: message});

});

