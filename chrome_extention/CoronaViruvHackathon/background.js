// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
// Tzahi Manistersky mailto:tzahimanmobile@gmail.com +972(52)2947775
// Use under public liscense of https://github.com/TzahiM/NeuroNet
// Specially contribiuted for corona virus hackathon. Dedicated for turn ideas into projects and results

// Called when the user clicks on the browser action.
chrome.browserAction.onClicked.addListener(function(tab) {
	
	
	var action_url = 'http://www.neuronetlabs.org/CoronaVirusHackathon/coplay/extention_add_with_url/?parent_url=';
	var parameters_url = tab.url + '&parent_url_text=' + tab.title;
	

	chrome.tabs.update(tab.id, { url: (action_url+ parameters_url)});

});

