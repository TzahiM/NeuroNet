// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.



// Called when the user clicks on the browser action.
// Called when the user clicks on the browser action.
chrome.browserAction.onClicked.addListener(function(tab) {
	
	
	//var action_url = 'http://kuterless.org.il/labs/coplay/add_with_url/?parent_url=';
//	var action_url = 'http://127.0.0.1:8000/CoronaVirusHackathon/coplay/add_with_url/?parent_url=';
	var action_url = 'http://www.neuronetlabs.org/CoronaVirusHackathon/coplay/add_with_url/?parent_url=';
	var parameters_url = tab.url + '&parent_url_text=' + tab.title;
	
	//		 http://kuterless.org.il/labs/coplay/add_with_url/?parent_url=http://www.kuterless.org.il/labs/coplay/578/details/&parent_url_text=%D7%A2%D7%95%D7%96%D7%A8%D7%99%D7%9D%20%D7%91%D7%9E%D7%A8%D7%97%D7%91%20%D7%A2%D7%91%D7%95%D7%93%D7%94%20%D7%A4%D7%AA%D7%95%D7%97%20%D7%91%D7%94%D7%95%D7%93%20%D7%94%D7%A9%D7%A8%D7%95%D7%9F%20%D7%9C%D7%94%D7%9E%D7%A6%D7%90%D7%95%D7%AA%20%D7%95%D7%A9%D7%99%D7%AA%D7%95%D7%A3%20%D7%A4%D7%A2%D7%95%D7%9C%D7%94,%20%D7%9C%D7%98%D7%95%D7%91%D7%AA%20%D7%94%D7%9B%D7%9C%D7%9C%20%D7%95%D7%91%D7%94%D7%A9%D7%A8%D7%90%D7%AA%20%D7%A7%D7%95%D7%93%20%D7%A4%D7%AA%D7%95%D7%97

	chrome.tabs.update(tab.id, { url: (action_url+ parameters_url)});

});

