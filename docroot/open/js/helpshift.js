Helpshift = {};

Helpshift.UI = function(){
	return {
		loadingbar : false,
		initialize : function(){
			$('#searchbox').fadeIn(100, function(){
				document.getElementById('searchinput').focus();
			if(window.location.search){
				document.getElementById('searchinput').value = window.location.search.split('=')[1].split('+')[0];
				Helpshift.SearchManager.get_search(true);
			}
			});
			
			
			//initialize UI here
		},
		load_result : function(search_obj){
			Helpshift.SearchManager.got_result(search_obj);
			Helpshift.UI.hide_loadingbar();
			var ele = document.getElementById("results");
			ele.innerHTML = "";
			if(search_obj.result_array.length == 0 && search_obj.relatedtopics_array.length == 0){
				ele.innerHTML = "<center>No results found</center>";
				return;
			}
			search_obj.result_array.forEach(function(res){ele.innerHTML = ele.innerHTML + ( res.format() || '' );})
			search_obj.relatedtopics_array.forEach(function(res){ele.innerHTML = ele.innerHTML + ( res.format() || '' );})
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
		},
		show_loadingbar : function(){
			if(Helpshift.UI.loadingbar == false){
				$('#loadingbar').fadeIn(1000);
				$('#lightbox').fadeIn(500);
				this.loadingbar = true;
			}
		},
		hide_loadingbar : function(){
			if(Helpshift.UI.loadingbar == true){
				$('#loadingbar').fadeOut(500);
				$('#lightbox').fadeOut(250);
				this.loadingbar = false;
			}
		},
	}
}();

Helpshift.SearchManager = function(){
	var query_result_map = {};
	var pending_query_map = {};
	var search_timer = "";
	return {
		new_search : function(event){
			clearTimeout(this.search_timer);
			if(event.type === 'keyup')
				this.search_timer = setTimeout(Helpshift.SearchManager.get_search, 1000);
			else if(event.type === 'change')
				Helpshift.SearchManager.get_search(active=true);
		},
		get_search : function(active){
			var ele = document.getElementById("searchinput");
			if(ele) var query = ele.value + "";
			query = query.trim();
			if(!query.length || pending_query_map[query])
				return;
			var result = query_result_map[query];
			if(!result)
				result = Helpshift.Search(query, active);
			else
				Helpshift.UI.load_result(result);
		},
		got_result : function(result){
			delete pending_query_map[result.query];
			query_result_map[result.query] = result;
		},
		made_request : function(query){
			pending_query_map[query] = true;
		},
	}
}();

Helpshift.Search = function(query, active){
	var self = {
		result_array : [],
		relatedtopics_array : [],
		query : "",
		_raw_result : {},
		set_result : function(res){
//			coonsole.log(res);
			if(res.status === "success"){
				if(typeof(res) === "string") 
					self._raw_result = JSON.parse(res.data);
				else
					self._raw_result = res.data;
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
			console.log(self._raw_result);
			Helpshift.UI.load_result(self);
		},
		parse_result_array : function(){
			self.Definition = self._raw_result
			self._raw_result.Results.forEach(function(res){self.result_array.push(Helpshift.Search.Result(self.query, res))});
			self._raw_result.RelatedTopics.forEach(function(relatedtopic){self.relatedtopics_array.push(Helpshift.Search.Result(self.query, relatedtopic))});
		},
		error : function(res){
			
			//error handling, retrying and cleanup if necessary here.
		},
		get_definition : function(){
			return self._raw_result.Definition;
		},
		get_definition_source : function(){
			return self._raw_result.DefinitionSource;
		},
		get_heading : function(){
			return self._raw_result.Heading;
		},
		get_abstract_source : function(){
			return self._raw_result.AbstractSource
		},
		get_image : function(){
			return self._raw_result.Image
		},
		get_abstract_text : function(){
			return self._raw_result.AbstractText
		},
		get_abstract : function(){
			return self._raw_result.Abstract
		},
		get_answer_type : function(){
			return self._raw_result.AnswerType
		},
		get_redirect : function(){
			return self._raw_result.Redirect
		},
		get_type : function(){
			return self._raw_result.Type
		},
		get_definitionURL : function(){
			return self._raw_result.DefinitionURL
		},
		get_answer : function(){
			return self._raw_result.Answer
		},
		get_definitionURL : function(){
			return self._raw_result.DefinitionURL
		},
	}
	self.query = query;
	if(active == true)
		Helpshift.UI.show_loadingbar();
	Helpshift.SearchManager.made_request(self.query);
	doXHR('/app/search/'+encodeURIComponent(self.query), self.set_result, self.error, console.log);
	return self;
}

Helpshift.Search.Result = function(query, relatedresult){
	
	var self = {
			query : "",
			domain : "",
			Result : "",
			Icon : {URL : '', Height: '', Width: ''},
			FirstURL : "",
			DisplayURL : "",
			Text : "",
			format : function(){
				var html = null;
				if(self.Result.length){
					html = "<div class='results_links highlight_2' onmouseover='this.setAttribute(\"class\",\"results_links highlight_2 highlight\");' onmouseout='this.setAttribute(\"class\",\"results_links highlight_2\");' style='margin-top: 5px;'>" +
							"<div class='icon_fav'>" +
							"<a onclick='fl=1;' href='/?q="+self.query+"site:www."+self.domain+"'>" +
							"<img title='www."+self.domain+"' alt='' src='"+self.Icon.URL+"' style='visibility: visible; ' width='"+( self.Icon.Width || 20)+"px' height='"+( self.Icon.Height || 20)+"px'>" +
							"</a></div><div class='links_main'>" +
							"<a class='large' href='"+self.FirstURL+"'>" +
							"<b>"+self.Text+"</b></a>" +
							"<div>" +
							"<a class='url' href='"+self.FirstURL+"'>"+(self.DisplayURL.split("www.")[1] || self.DisplayURL.split("http://")[1] || self.DisplayURL.split("/")[1] || self.DisplayURL)+"</a> &nbsp; " +
							"<a href='/?q="+self.query+"+site:"+self.domain+"' title='Search domain "+self.domain+"' class='links_menu'>More results</a></div></div>" +
							"<div class='clear'></div></div>"
				}
				return html;
			},
	}
	self.Result = relatedresult.Result || "";
	self.Icon = relatedresult.Icon || "";
	self.FirstURL = relatedresult.FirstURL || "";
	self.DisplayURL = "http://"+self.FirstURL.split('__slashslash__')[1]; 
	self.Text = relatedresult.Text || "";
	self.domain = self.FirstURL.split('www.')[1] || self.FirstURL.split('http://')[1] || self.FirstURL || "";
	self.domain = self.domain.split('/')[0] || self.FirstURL || "";
	self.query = query;
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
	return retval;
}