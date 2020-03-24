// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.


// Called when the user clicks on the browser action.
chrome.browserAction.onClicked.addListener(function(tab) {
	
	
	var action_url = 'http://kuterless.org.il/labs/coplay/add_with_url/?parent_url=';

	var parameters_url = tab.url + '&parent_url_text=' + tab.title;
	
	chrome.tabs.update(tab.id, { url: (action_url+ parameters_url)});

});

