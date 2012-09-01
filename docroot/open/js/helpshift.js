Helpshift = {};

Helpshift.Admin = function() {
	/*
	 * Admin singleton object
	 * Handles getting data and populating it at the right place.
	 * Also sets Interval so that data is dynamically updated.
	 */
	return {
		interval1 : null,
		interval2 : null,
		get_data : function() {
			/*
			 * Loads everything.Initial call after loading.
			 */
			Helpshift.Admin.get_site_data();
			Helpshift.Admin.get_user_data();
		},
		get_site_data : function() {
			/*
			 * Get site data.
			 */
			clearInterval(Helpshift.Admin.interval1);
			doXHR('/app/admin/getsitedata/', Helpshift.Admin.got_site_data, Helpshift.Admin.error, console.log);
			Helpshift.Admin.interval1 = setInterval(Helpshift.Admin.get_site_data, 5000);
		},
		get_url_data : function(url) {
			/*
			 * Gets site data but for a specific URL.
			 */
			clearInterval(Helpshift.Admin.interval1);
			url = url.replace('//', "__slashslash__");
			if (url) {
				doXHR('/app/admin/getsitedata/' + url, Helpshift.Admin.got_url_data, Helpshift.Admin.error, console.log);
				Helpshift.Admin.interval1 = setInterval(function() {
					Helpshift.Admin.get_url_data(url)
				}, 5000);
			}
		},
		get_user_data : function() {
			/*
			 * Gets all user data.
			 */
			clearInterval(Helpshift.Admin.interval2);
			doXHR('/app/admin/getuserdata/', Helpshift.Admin.got_user_data, Helpshift.Admin.error, console.log);
			Helpshift.Admin.interval2 = setInterval(Helpshift.Admin.get_user_data, 5000);
		},
		get_spec_user_data : function(user) {
			/*
			 * Gets data of a specific user.
			 */
			clearInterval(Helpshift.Admin.interval2);
			if (user) {
				doXHR('/app/admin/getuserdata/' + user, Helpshift.Admin.got_spec_user_data, Helpshift.Admin.error, console.log);
				Helpshift.Admin.interval2 = setInterval(function() {
					Helpshift.Admin.get_spec_user_data(user)
				}, 5000);
			}
		},
		got_site_data : function(resp) {
			/*
			 * Callback for get_side_data.
			 */
			if ( typeof (resp) === "string") {
				try {
					resp = JSON.parse(resp);
				} catch (e) {
					return;
				}
			}
			var ele = document.getElementById("site_data_list");
			if (ele) {
				ele.innerHTML = "<li style='height:25px;margin-top:5px;width:100%;position:relative;margin:0px 10% 0px 0px;font-size:20px;font-weight:bold;'><div style='position:relative;float:left;'>URL</div><div style='position:relative;float:right;'>Count</div></li>";
				resp.site_data.forEach(function(data) {
					for (key in data) {
						html = '<li onclick="Helpshift.Admin.get_url_data(\'' + key + '\');" style="height:25px;margin-bottom:6px;cursor:pointer;width:100%;position:relative;">'
						html = html + '<div style="height:25px;margin-top:5px;border-bottom:1px solid grey;width:50%;position:relative;float:left;" title="Click for time and user details of ';
						html = html + key + '">' + key + '</div><div style="height:25px;margin-top:5px;border-bottom:1px solid grey;width:50%;text-align:right;position:relative;float:right;" title="Click for time and user details of ';
						html = html + key + '">' + data[key] + '</div></li>';
						ele.innerHTML = ele.innerHTML + html;
					}
				});
			}
		},
		got_user_data : function(resp) {
			/*
			 * Callback for get_user_data.
			 */
			if ( typeof (resp) === "string") {
				try {
					resp = JSON.parse(resp);
				} catch (e) {
					return;
				}
			}
			var ele = document.getElementById("user_data_list");
			if (ele) {
				ele.innerHTML = "<li style='height:25px;margin-top:5px;font-size:20px;font-weight:bold;'>List of Users:</li>";
				resp.user_data.forEach(function(data) {
					html = '<li onclick="Helpshift.Admin.get_spec_user_data(\'' + data + '\');" style="cursor:pointer;height:25px;margin-top:5px;">';
					html = html + '<div style="height:25px;margin-top:5px;position:relative;border-bottom:1px solid grey;width:100%;text-align:left;" title="See details of ' + data + '">' + data + '</div></li>';
					ele.innerHTML = ele.innerHTML + html;
				});
			}
		},
		got_url_data : function(resp) {
			/*
			 * Callback for get_url_data.
			 */
			if ( typeof (resp) === "string") {
				try {
					resp = JSON.parse(resp);
				} catch (e) {
					return;
				}
			}
			var ele = document.getElementById("site_data_list");
			if (ele) {
				ele.innerHTML = "<li style='height:25px;margin-top:5px;width:100%;position:relative;margin:0px 10% 0px 0px;font-size:16px;font-weight:bold;'><div style='position:relative;float:left;color:blue;'><font style='color:grey'>Data for URL:</font>" + resp.url + "</div><div style='position:relative;float:right;'></div></li>";
				ele.innerHTML = ele.innerHTML + "<li style='height:25px;margin-top:5px;width:100%;position:relative;font-size:20px;font-weight:bold;'><div style='height:25px;margin-top:5px;position:relative;float:left;'>User</div><div style='height:25px;margin-top:5px;position:relative;float:right;'>Date, Time</div></li>"
				resp.site_data.forEach(function(data) {
					data = [data.split("'")[1], data.split("'")[3], data.split("'")[5]];
					html = '<li onclick="Helpshift.Admin.get_site_data();" style="height:25px;margin-bottom:5px;cursor:pointer;width:100%;position:relative;border-bottom:1px solid grey;">';
					html = html + '<div title="Click to see list of all URLs and count" style="height:25px;margin-top:5px;position:relative;float:left;">' + data[0] + '</div>';
					html = html + '<div title="Click to see list of all URLs and count" style="height:25px;margin-top:5px;text-align:right;position:relative;float:right;">';
					html = html + data[1] + ", " + data[2] + '</div></li>';
					ele.innerHTML = ele.innerHTML + html;
				});
			}
		},
		got_spec_user_data : function(resp) {
			/*
			 * Callback for get_spec_user_data.
			 */
			if ( typeof (resp) === "string") {
				try {
					resp = JSON.parse(resp);
				} catch (e) {
					return;
				}
			}
			var ele = document.getElementById("user_data_list");
			if (ele) {
				ele.innerHTML = "<li style='height:25px;margin-top:5px;font-size:16px;font-weight:bold;color:blue;'><font style='color:grey'>Details for User:</font>" + resp.user + "</li>";
				ele.innerHTML = ele.innerHTML + "<li style='height:25px;margin-top:5px;width:100%;position:relative;font-size:20px;font-weight:bold;'><div style='position:relative;float:left;'>URL</div><div style='position:relative;float:right;'>Date, Time</div></li>"
				resp.user_data.forEach(function(data){
					for (key in data){
						date_time = [data[key].split("'")[1], data[key].split("'")[3]];
						ele.innerHTML = ele.innerHTML + '<li onclick="Helpshift.Admin.get_user_data();" style="height:25px;margin-top:5px;cursor:pointer;width:100%;position:relative;margin:0px 10% 0px 0px"><div title="Click to see list of all users" style="height:25px;margin-top:5px;position:relative;float:left;border-bottom:1px solid grey;width:50%;">' + key + '</div><div title="Click to see list of all users" style="height:25px;margin-top:5px;position:relative;float:right;border-bottom:1px solid grey;width:50%;text-align:right;">' + date_time[0] +', '+ date_time[1] + '</div></li>';
					}	
				});
				
			}
		},
		error : function() {
			/*
			 *Logs a error message.
			 */
			Helpshift.UI.error("Some error in getting data from Admin.");
		}
	}
}();

Helpshift.UI = function() {
	return {
		loadingbar : false,
		initialize : function() {
			$('#searchbox').fadeIn(100, function() {
				document.getElementById('searchinput').focus();
				setTimeout(function() {
					$('#admin_img').fadeIn(100, function() {
						document.getElementById('admin_img').setAttribute("class", "animated wiggle");
						setTimeout(function() {
							document.getElementById('admin_img').setAttribute("class", "admin_img");
						}, 1000);
					});
				}, 5000);
				if (window.location.search) {
					document.getElementById('searchinput').value = window.location.search.split('=')[1].split('+')[0];
					Helpshift.SearchManager.get_search(true);
				}
			});
			//initialize UI here
		},
		load_result : function(search_obj) {
			Helpshift.SearchManager.got_result(search_obj);
			Helpshift.UI.hide_loadingbar();
			var ele = document.getElementById("results");
			if (ele) {
				ele.innerHTML = "";
				if (search_obj.result_array.length == 0 && search_obj.relatedtopics_array.length == 0) {
					ele.innerHTML = "<center>No results found</center>";
					return;
				}
				search_obj.result_array.forEach(function(res) {
					ele.innerHTML = ele.innerHTML + (res.format() || '' );
				})
				search_obj.relatedtopics_array.forEach(function(res) {
					ele.innerHTML = ele.innerHTML + (res.format() || '' );
				})
			}
			//load result here
		},
		show_loadingbar : function() {
			if (Helpshift.UI.loadingbar == false) {
				$('#loadingbar').fadeIn(1000);
				$('#lightbox').fadeIn(500);
				this.loadingbar = true;
			}
		},
		hide_loadingbar : function() {
			if (Helpshift.UI.loadingbar == true) {
				$('#loadingbar').fadeOut(500);
				$('#lightbox').fadeOut(250);
				this.loadingbar = false;
			}
		},
		error : function(msg){
			var parent = document.getElementById('index');
			notification_dom = dojo.create('div', { id: "notification", class: "notification"}, parent);
			html = "<div style='margin: 7px 0px 7px 20px;float: left;'><span><font size='2' face='courier' color=white>"+ msg +"</font><span></div><img src='/images/close_button.png' style='width:16px;height: 16px;float:right;margin: 7px 10px; cursor:pointer;' onclick='dojo.destroy(\"notification\")'></img>"
			notification_dom.innerHTML = html;
			setTimeout(function(){ dojo.destroy("notification"); }, 2000);
		}
	}
}();

Helpshift.SearchManager = function() {
	/*
	 * Healpshift.SearchManager is responsible to request searches and save Helpshift.Search objects in the search 
	 */
	var query_result_map = {};
	var pending_query_map = {};
	var search_timer = "";
	return {
		new_search : function(event) {
			/*
			 * Listens to events.Checks type of events to decide if it is a silent query or an active one.
			 * An active query shows loading bar.
			 * 
			 * Inactive query happen only when the user shows an inactivity of 1 second.
			 */
			clearTimeout(this.search_timer);
			if (event.type === 'keyup')
				this.search_timer = setTimeout(Helpshift.SearchManager.get_search, 1000);
			else if (event.type === 'change')
				Helpshift.SearchManager.get_search( active = true);
		},
		get_search : function(active) {
			/*
			 * Checks the internal data structures for the requested query.
			 * If present loads it, otherwise makes the creates a new Helpshift.Search object with the query. 
			 */
			var ele = document.getElementById("searchinput");
			if (ele)
				var query = ele.value + "";
			query = query.trim();
			if (!query.length || pending_query_map[query])
				return;
			var result = query_result_map[query];
			if (!result)
				result = Helpshift.Search(query, active);
			else
				Helpshift.UI.load_result(result);
		},
		got_result : function(result) {
			/*
			 * Updates structures with the new result recieved.
			 * Deletes entry from pending_query_map
			 * Makes entry in query_result_map.
			 * Also sets up a timeout for cleanup of query.Value at the moment is 5mins.
			 * Should be given by the server maybe.  
			 */
			delete pending_query_map[result.query];
			query_result_map[result.query] = result;
			setTimeout(function(){
				Helpshift.SearchManager.del_query(result.query);
			}, 300000)
		},
		made_request : function(query) {
			/*
			 * Saves every query in progress so as to avoid multiple requests.
			 */
			pending_query_map[query] = true;
		},
		del_query : function(query){
			/*
			 * Deletes the given query from the query_result_map.
			 * 
			 * And also from pending_result_map(just in case).
			 */
			try{
				delete query_result_map[result.query];	
			}catch(e){
				
			}
			try{
				delete pending_query_map[result.query];	
			}catch(e){
				
			}
		}
	}
}();

Helpshift.Search = function(query, active) {
	/*
	 * Search Object.
	 * Every unique query creates a new search object.
	 * The search object saves the raw_result from the Search API, 
	 * parses it to create Helpshift.Result objects and populates its own data also.
	 */
	var self = {
		result_array : [],
		relatedtopics_array : [],
		query : "",
		_raw_result : {},
		set_result : function(res) {
			//			coonsole.log(res);
			if (res.status === "success") {
				if ( typeof (res) === "string") {
					try {
						self._raw_result = JSON.parse(res.data);
					} catch (e) {
						self.error("Error in parsing data from server");
					}
				} else
					self._raw_result = res.data;
				self.process_result();
			} else
				self.error("Error recieved from Server:"+res.data);
		},
		get_result : function() {
			return self._raw_result;
		},
		process_result : function() {
			self.parse_result_array();
			console.log(self._raw_result);
			Helpshift.UI.load_result(self);
		},
		parse_result_array : function() {
			self.Definition = self._raw_result
			self._raw_result.Results.forEach(function(res) {
				self.result_array.push(Helpshift.Search.Result(self.query, res))
			});
			self._raw_result.RelatedTopics.forEach(function(relatedtopic) {
				self.relatedtopics_array.push(Helpshift.Search.Result(self.query, relatedtopic))
			});
		},
		error : function(msg) {
			Helpshift.SearchManager.del_query(self.query);
			Helpshift.UI.error(msg);		//Inform user.
			//error handling, retrying and cleanup if necessary here.
		},
		get_definition : function() {
			return self._raw_result.Definition;
		},
		get_definition_source : function() {
			return self._raw_result.DefinitionSource;
		},
		get_heading : function() {
			return self._raw_result.Heading;
		},
		get_abstract_source : function() {
			return self._raw_result.AbstractSource
		},
		get_image : function() {
			return self._raw_result.Image
		},
		get_abstract_text : function() {
			return self._raw_result.AbstractText
		},
		get_abstract : function() {
			return self._raw_result.Abstract
		},
		get_answer_type : function() {
			return self._raw_result.AnswerType
		},
		get_redirect : function() {
			return self._raw_result.Redirect
		},
		get_type : function() {
			return self._raw_result.Type
		},
		get_definitionURL : function() {
			return self._raw_result.DefinitionURL
		},
		get_answer : function() {
			return self._raw_result.Answer
		},
		get_definitionURL : function() {
			return self._raw_result.DefinitionURL
		},
	}
	self.query = query;
	if (active == true)
		Helpshift.UI.show_loadingbar();
	Helpshift.SearchManager.made_request(self.query);
	doXHR('/app/search/' + encodeURIComponent(self.query), self.set_result, self.error, console.log);
	return self;
}

Helpshift.Search.Result = function(query, relatedresult) {
/*
 * Result object.
 * Helps in parsing and formatting of results.
 */
	var self = {
		query : "",
		domain : "",
		Result : "",
		Icon : {
			URL : '',
			Height : '',
			Width : ''
		},
		FirstURL : "",
		DisplayURL : "",
		Text : "",
		format : function() {
			var html = null;
			if (self.Result.length) {
				html = "<div class='results_links highlight_2' onmouseover='this.setAttribute(\"class\",\"results_links highlight_2 highlight\");' onmouseout='this.setAttribute(\"class\",\"results_links highlight_2\");' style='margin-top: 5px;'>" + "<div class='icon_fav'>" + "<a onclick='fl=1;' href='/?q=" + self.query + "site:www." + self.domain + "'>" + "<img title='www." + self.domain + "' alt='' src='" + self.Icon.URL + "' style='visibility: visible; ' width='" + (self.Icon.Width || 20) + "px' height='" + (self.Icon.Height || 20) + "px'>" + "</a></div><div class='links_main'>" + "<a class='large' href='" + self.FirstURL + "'>" + "<b>" + self.Text + "</b></a>" + "<div>" + "<a class='url' href='" + self.FirstURL + "'>" + (self.DisplayURL.split("www.")[1] || self.DisplayURL.split("http://")[1] || self.DisplayURL.split("/")[1] || self.DisplayURL) + "</a> &nbsp; " + "<a href='/?q=" + self.query + "+site:" + self.domain + "' title='Search domain " + self.domain + "' class='links_menu'>More results</a></div></div>" + "<div class='clear'></div></div>"
			}
			return html;
		},
	}
	self.Result = relatedresult.Result || "";
	self.Icon = relatedresult.Icon || "";
	self.FirstURL = relatedresult.FirstURL || "";
	self.DisplayURL = "http://" + self.FirstURL.split('__slashslash__')[1];
	self.Text = relatedresult.Text || "";
	self.domain = self.FirstURL.split('www.')[1] || self.FirstURL.split('http://')[1] || self.FirstURL || "";
	self.domain = self.domain.split('/')[0] || self.FirstURL || "";
	self.query = query;
	return self
}
//Helper functions//
function doXHR(url, success, failure, logger) {
	/*
	 * Takes url, success callback, failure callback and logger.
	 * Make async requests to the specified url.
	 * Uses dojo library.
	 */
	var xhrArgs = {
		url : url,
		handleAs : "json",
		preventCache : true,
		load : success,
		error : function(err, ioArgs) {
			if (err.dojoType == 'cancel')
				return;
			else
				failure(err, ioArgs);
		}
	};
	var retval = dojo.xhrGet(xhrArgs);
	return retval;
}
