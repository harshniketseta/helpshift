Helpshift = {};

Helpshift.UI = function(){
	return {
		initialize : function(){
			$('#searchbox').slideDown(function(){
				document.getElementById('searchinput').focus();	
			});
			
			
			//initialize UI here
		},
		load_result : function(search_obj){
			var ele = document.getElementById("results")
			search_obj.result_array.forEach(function(res){ele.innerHTML = ele.innerHTML + res.format();}) 
			//load result here
		},
		toggle : function(ele){
			if(typeof(ele) === "string")
				var ele = document.getElementById(ele);
			switch (ele.id) {
			case 'loadingbar':
				if(ele.style.display === "none"){
					$('#loadingbar').fadeIn(1000);
					$('#lightbox').fadeIn(500);
				}
				else{
					$('#loadingbar').fadeOut(500);
					$('#lightbox').fadeOut(250);
				}
				break;

			default:
				break;
			}
		}
	}
}();

Helpshift.SearchManager = function(){
	var query_result_map = {};
	var search_timer = "";
	return {
		new_search : function(event){
			if(event.type === 'keyup'){
				clearTimeout(this.search_timer);
				this.search_timer = setTimeout(Helpshift.SearchManager.get_search, 1000)
			}
			else if(event.type === 'change')
				Helpshift.SearchManager.get_search();
		},
		get_search : function(){
			var ele = document.getElementById("searchinput");
			if(ele) query = ele.value + "";
			query = query.trim();
			if(!query.length)
				return;
			
			var result = query_result_map[query];
			if(!result){
				result = Helpshift.Search(query);
				query_result_map[query] = result;
			}
			else
				Helpshift.UI.load_result(result);
		}
	}
}();

Helpshift.Search = function(query){
	var self = {
		result_array : [],
		query : "",
		_raw_result : {},
		set_result : function(res){
//			coonsole.log(res);
			if(res.status === "success"){
				self._raw_result = JSON.parse(res.data);
				self.process_result();
			}
			else
				self.error(res)
		},
		get_result : function(){
			return self._raw_result;
		},
		process_result : function(){
			self.parse_result_array();
			Helpshift.UI.toggle('loadingbar');
			console.log(self._raw_result)
			document.getElementById("results").innerHTML = JSON.toString(self._raw_result);
			Helpshift.UI.load_result(self);
		},
		parse_result_array : function(){
			self._raw_result.RelatedTopics.forEach(function(relatedtopic){self.result_array.push(Helpshift.Search.Result(relatedtopic))});
		},
		error : function(res){
			
			//error handling, retrying and cleanup if necessary here.
		}
	}
	self.query = query;
	Helpshift.UI.toggle('loadingbar');
	doXHR('/main/search/'+encodeURIComponent(self.query), self.set_result, self.error, console.log);
	return self;
}

Helpshift.Search.Result = function(relatedresult){
	
	var self = {
			Result : "",
			Icon : {URL : '', Height: '', Width: ''},
			FirstURL : "",
			Text : "",
			format : function(){
				html = "<div id='r1-4' class='results_links_deep highlight_d2 highlight'>";
				if(self.Icon.URL.length && self.Icon.Height.length && self.Icon.Width.length)
					html = html + "<div class='icon_fav2'>" +
						"<a href='"+self.Icon.FirstURL+"' title=''>" +
						"<img title='' alt='' src='"+self.Icon.URL+"+' style='visibility: visible; ' width='"+self.Icon.Width+"' height='"+self.Icon.Height+"'>" +
						"</a>" + "</div>";
					html = html + "<div class='links_main links_deep'><h2><a class='large' href='"+self.FirstURL+"'>" +
						"Yellowstone " +
						"<b>" +
						"National Park" +
						"</b>" +
						" ~ The Total Yellowstone Page" +
						"</a>" +
						"</h2>" +
						"<div class='snippet'>'A thousand Yellowstone wonders are calling, 'Look up and down and round about you!'' John Muir - 1898" +
						"</div>" +
						"<div>" +
						"<a href='http://www.valley-forge.national-park.com/' class='url'> valley-forge.national-park.com" +
						"</a>&nbsp; &nbsp;" +
						"<a href='/?q=valley%20forge%20national%20park+site:www.valley-forge.national-park.com' title='Search domain www.valley-forge.national-park.com' class='links_menu hidden2'>" +
						"More results" +
						"</a>" +
						"</div>" +
						"</div>" +
						"</div>";
			},
	}
	self.Result = relatedresult.Result;
	self.Icon = relatedresult.Icon;
	self.FirstURL = relatedresult.FirstURL;
	self.Text = relatedresult.Text;
	return self
}

//Helper functions//
function doXHR(url, success, failure, logger){
	var xhrArgs = {
		url: url,
		handleAs: "json",
		preventCache: true,
		load: success,
		error: function(err, ioArgs){
				if (err.dojoType == 'cancel') 
					return;
				else 
					failure(err, ioArgs);
			}
	};
	var retval = dojo.xhrGet(xhrArgs);
	// retval.abort = function() { logger(SPARX.Logger.DEBUG, 'here'); try { this.cancel(); } catch(e) {} };
	return retval;
}