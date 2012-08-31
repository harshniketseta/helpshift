def wrap_links(response):
    '''
    At the moment wrapping links according to DuckDuckGo structure.
    '''
    data = response['data']
    response['data'] = recursive_dict_wrap(data)
    return response

def recursive_dict_wrap(data):
    for key, value in data.iteritems():
        print "In dict_wrap", key , value , type(value)
        if isinstance(value, dict):
            print "calling recursive_dict_wrap"
            data[key] = recursive_dict_wrap(value)
        if isinstance(value, list):
            print "calling recursive_list_wrap"
            data[key] = recursive_list_wrap(value)
        else:
            print "setting ", key, "with value ", value
            data[key] = value
    print "retruning from  recursive_dict_wrap:", data
    return data

def recursive_list_wrap(data):
    new_data = []
    for d in data:
        print "In list_wrap", d , type(d)
        if isinstance(d, dict):
            print "calling recursive_dict_wrap"
            new_data.append(recursive_dict_wrap(d))
        if isinstance(d, list):
            print "calling recursive_list_wrap"
            new_data.append(recursive_list_wrap(d))
        else:
            new_data.append(d)
    print "retruning from  recursive_list_wrap:", new_data
    return new_data

response = dict(status="success", data={
   "Definition" : "chrome definition: chromium.",
   "DefinitionSource" : "Merriam-Webster",
   "Heading" : "Chrome",
   "AbstractSource" : "Wikipedia",
   "Image" : "",
   "RelatedTopics" : [
      {
         "Result" : "<a href=\"http://duckduckgo.com/Google_Chrome\">Google Chrome</a>, a web browser",
         "Icon" : {
            "URL" : "https://i.duckduckgo.com/i/6e9059f3.png",
            "Height" : "",
            "Width" : ""
         },
         "FirstURL" : "http://duckduckgo.com/Google_Chrome",
         "Text" : "Google Chrome, a web browser"
      },
      {
         "Result" : "<a href=\"http://duckduckgo.com/Google_Chrome_OS\">Google Chrome OS</a>, a web-centric Linux-based operating system",
         "Icon" : {
            "URL" : "https://i.duckduckgo.com/i/bd51c11c.png",
            "Height" : "",
            "Width" : ""
         },
         "FirstURL" : "http://duckduckgo.com/Google_Chrome_OS",
         "Text" : "Google Chrome OS, a web-centric Linux-based operating system"
      },
      {
         "Result" : "<a href=\"http://duckduckgo.com/Chromium\">Chromium</a>, a chemical element",
         "Icon" : {
            "URL" : "https://i.duckduckgo.com/i/78256602.jpg",
            "Height" : "",
            "Width" : ""
         },
         "FirstURL" : "http://duckduckgo.com/Chromium",
         "Text" : "Chromium, a chemical element"
      },
      {
         "Topics" : [
            {
               "Result" : "<a href=\"http://duckduckgo.com/Chrome_plating\">Chrome plating</a>, a process of surfacing with chromium",
               "Icon" : {
                  "URL" : "https://i.duckduckgo.com/i/fa0d2019.jpg",
                  "Height" : "",
                  "Width" : ""
               },
               "FirstURL" : "http://duckduckgo.com/Chrome_plating",
               "Text" : "Chrome plating, a process of surfacing with chromium"
            }
         ],
         "Name" : "Materials"
      },
      {
         "Topics" : [
            {
               "Result" : "<a href=\"http://duckduckgo.com/oxygene_(programming_language)\">Chrome (programming language)</a> or Oxygene, an Object Pascal implementation for the .NET Framework",
               "Icon" : {
                  "URL" : "https://i.duckduckgo.com/i/23afc700.png",
                  "Height" : "",
                  "Width" : ""
               },
               "FirstURL" : "http://duckduckgo.com/oxygene_(programming_language)",
               "Text" : "Chrome (programming language) or Oxygene, an Object Pascal implementation for the .NET Framework"
            },
            {
               "Result" : "<a href=\"http://duckduckgo.com/User_interface_chrome\">User interface chrome</a>, the borders and widgets that frame the content part of a window",
               "Icon" : {
                  "URL" : "",
                  "Height" : "",
                  "Width" : ""
               },
               "FirstURL" : "http://duckduckgo.com/User_interface_chrome",
               "Text" : "User interface chrome, the borders and widgets that frame the content part of a window"
            },
            {
               "Result" : "<a href=\"http://duckduckgo.com/xUL\">Chrome Mozilla</a> or XUL, the Mozilla XML user interface language",
               "Icon" : {
                  "URL" : "https://i.duckduckgo.com/i/32178d88.png",
                  "Height" : "",
                  "Width" : ""
               },
               "FirstURL" : "http://duckduckgo.com/xUL",
               "Text" : "Chrome Mozilla or XUL, the Mozilla XML user interface language"
            },
            {
               "Result" : "<a href=\"http://duckduckgo.com/S3_Chrome\">S3 Chrome</a>, a series of graphics accelerators",
               "Icon" : {
                  "URL" : "https://i.duckduckgo.com/i/31ad53aa.jpg",
                  "Height" : "",
                  "Width" : ""
               },
               "FirstURL" : "http://duckduckgo.com/S3_Chrome",
               "Text" : "S3 Chrome, a series of graphics accelerators"
            },
            {
               "Result" : "<a href=\"http://duckduckgo.com/Microsoft_Chrome\">Microsoft Chrome</a>, an API for DirectX",
               "Icon" : {
                  "URL" : "",
                  "Height" : "",
                  "Width" : ""
               },
               "FirstURL" : "http://duckduckgo.com/Microsoft_Chrome",
               "Text" : "Microsoft Chrome, an API for DirectX"
            }
         ],
         "Name" : "Computing"
      },
      {
         "Topics" : [
            {
               "Result" : "<a href=\"http://duckduckgo.com/Chrome_(XM)\">Chrome (XM)</a>, a former music satellite channel",
               "Icon" : {
                  "URL" : "https://i.duckduckgo.com/i/ce375f83.png",
                  "Height" : "",
                  "Width" : ""
               },
               "FirstURL" : "http://duckduckgo.com/Chrome_(XM)",
               "Text" : "Chrome (XM), a former music satellite channel"
            },
            {
               "Result" : "<a href=\"http://duckduckgo.com/Chrome_(band)\">Chrome (band)</a>, a band from San Francisco",
               "Icon" : {
                  "URL" : "https://i.duckduckgo.com/i/7c48cfae.jpg",
                  "Height" : "",
                  "Width" : ""
               },
               "FirstURL" : "http://duckduckgo.com/Chrome_(band)",
               "Text" : "Chrome (band), a band from San Francisco"
            },
            {
               "Result" : "<a href=\"http://duckduckgo.com/Chrome_(Catherine_Wheel_album)\">Chrome (Catherine Wheel album)</a> - Chrome is the second full-length album by the English alternative rock band Catherine Wheel, released in 1993.",
               "Icon" : {
                  "URL" : "https://i.duckduckgo.com/i/acd10b2b.jpg",
                  "Height" : "",
                  "Width" : ""
               },
               "FirstURL" : "http://duckduckgo.com/Chrome_(Catherine_Wheel_album)",
               "Text" : "Chrome (Catherine Wheel album) - Chrome is the second full-length album by the English alternative rock band Catherine Wheel, released in 1993."
            },
            {
               "Result" : "<a href=\"http://duckduckgo.com/Chrome_(Trace_Adkins_album)\">Chrome (Trace Adkins album)</a> - Chrome is the fourth studio album by American country music singer Trace Adkins.",
               "Icon" : {
                  "URL" : "https://i.duckduckgo.com/i/75e873b1.jpg",
                  "Height" : "",
                  "Width" : ""
               },
               "FirstURL" : "http://duckduckgo.com/Chrome_(Trace_Adkins_album)",
               "Text" : "Chrome (Trace Adkins album) - Chrome is the fourth studio album by American country music singer Trace Adkins."
            },
            {
               "Result" : "<a href=\"http://duckduckgo.com/Chrome_(Trace_Adkins_song)\">\"Chrome\" (Trace Adkins song)</a> - \"Chrome\" is the title of a song written by Anthony Smith and Jeffrey Steele, and recorded by American country music artist Trace Adkins.",
               "Icon" : {
                  "URL" : "https://i.duckduckgo.com/i/42aab548.jpg",
                  "Height" : "",
                  "Width" : ""
               },
               "FirstURL" : "http://duckduckgo.com/Chrome_(Trace_Adkins_song)",
               "Text" : "\"Chrome\" (Trace Adkins song) - \"Chrome\" is the title of a song written by Anthony Smith and Jeffrey Steele, and recorded by American country music artist Trace Adkins."
            },
            {
               "Result" : "<a href=\"http://duckduckgo.com/Chrome_(Debbie_Harry_song)\">\"Chrome\" (Debbie Harry song)</a>, a song by Debbie Harry from Koo Koo",
               "Icon" : {
                  "URL" : "",
                  "Height" : "",
                  "Width" : ""
               },
               "FirstURL" : "http://duckduckgo.com/Chrome_(Debbie_Harry_song)",
               "Text" : "\"Chrome\" (Debbie Harry song), a song by Debbie Harry from Koo Koo"
            }
         ],
         "Name" : "Music"
      },
      {
         "Topics" : [
            {
               "Result" : "<a href=\"http://duckduckgo.com/Chrome%2C_California\">Chrome, California</a>, a community in Glenn County",
               "Icon" : {
                  "URL" : "",
                  "Height" : "",
                  "Width" : ""
               },
               "FirstURL" : "http://duckduckgo.com/Chrome%2C_California",
               "Text" : "Chrome, California, a community in Glenn County"
            }
         ],
         "Name" : "Places"
      },
      {
         "Topics" : [
            {
               "Result" : "<a href=\"http://duckduckgo.com/Chrome_Engine\">Chrome Engine</a>, a game engine developed by Techland",
               "Icon" : {
                  "URL" : "https://i.duckduckgo.com/i/d0263171.jpg",
                  "Height" : "",
                  "Width" : ""
               },
               "FirstURL" : "http://duckduckgo.com/Chrome_Engine",
               "Text" : "Chrome Engine, a game engine developed by Techland"
            },
            {
               "Result" : "<a href=\"http://duckduckgo.com/Chrome_(video_game)\">Chrome (video game)</a>, a sci-fi first-person shooter by Techland",
               "Icon" : {
                  "URL" : "https://i.duckduckgo.com/i/ba2caa80.jpg",
                  "Height" : "",
                  "Width" : ""
               },
               "FirstURL" : "http://duckduckgo.com/Chrome_(video_game)",
               "Text" : "Chrome (video game), a sci-fi first-person shooter by Techland"
            },
            {
               "Result" : "<a href=\"http://duckduckgo.com/Jenny_Swensen\">Jenny Swensen</a>, or Chrome, a Marvel Comics female paranormal character",
               "Icon" : {
                  "URL" : "https://i.duckduckgo.com/i/b485ef80.jpg",
                  "Height" : "",
                  "Width" : ""
               },
               "FirstURL" : "http://duckduckgo.com/Jenny_Swensen",
               "Text" : "Jenny Swensen, or Chrome, a Marvel Comics female paranormal character"
            },
            {
               "Result" : "<a href=\"http://duckduckgo.com/Chrome_(comics)\">Chrome (comics)</a>, or Allen Marc Yuricic, a Marvel Comics male mutant character",
               "Icon" : {
                  "URL" : "https://i.duckduckgo.com/i/43ec7438.jpg",
                  "Height" : "",
                  "Width" : ""
               },
               "FirstURL" : "http://duckduckgo.com/Chrome_(comics)",
               "Text" : "Chrome (comics), or Allen Marc Yuricic, a Marvel Comics male mutant character"
            }
         ],
         "Name" : "Games and fiction"
      },
      {
         "Topics" : [
            {
               "Result" : "<a href=\"http://duckduckgo.com/d/Chromium\">Chromium Meanings</a>",
               "Icon" : {
                  "URL" : "",
                  "Height" : "",
                  "Width" : ""
               },
               "FirstURL" : "http://duckduckgo.com/d/Chromium",
               "Text" : "Chromium Meanings"
            },
            {
               "Result" : "<a href=\"http://duckduckgo.com/Chromium_(web_browser)\">Chromium (web browser)</a>, the open source counterpart to Google Chrome",
               "Icon" : {
                  "URL" : "https://i.duckduckgo.com/i/f40b9f33.png",
                  "Height" : "",
                  "Width" : ""
               },
               "FirstURL" : "http://duckduckgo.com/Chromium_(web_browser)",
               "Text" : "Chromium (web browser), the open source counterpart to Google Chrome"
            },
            {
               "Result" : "<a href=\"http://duckduckgo.com/Chromium_OS\">Chromium OS</a>, the open source counterpart to Google Chrome OS",
               "Icon" : {
                  "URL" : "https://i.duckduckgo.com/i/f40b9f33.png",
                  "Height" : "",
                  "Width" : ""
               },
               "FirstURL" : "http://duckduckgo.com/Chromium_OS",
               "Text" : "Chromium OS, the open source counterpart to Google Chrome OS"
            },
            {
               "Result" : "<a href=\"http://duckduckgo.com/Google_Chrome_Frame\">Google Chrome Frame</a>, an Internet Explorer plug-in based on Chromium",
               "Icon" : {
                  "URL" : "https://i.duckduckgo.com/i/f6b2e6bc.png",
                  "Height" : "",
                  "Width" : ""
               },
               "FirstURL" : "http://duckduckgo.com/Google_Chrome_Frame",
               "Text" : "Google Chrome Frame, an Internet Explorer plug-in based on Chromium"
            },
            {
               "Result" : "<a href=\"http://duckduckgo.com/Chromite\">Chromite</a>, a mineral ore from which chromium is produced",
               "Icon" : {
                  "URL" : "https://i.duckduckgo.com/i/21cee4c0.jpg",
                  "Height" : "",
                  "Width" : ""
               },
               "FirstURL" : "http://duckduckgo.com/Chromite",
               "Text" : "Chromite, a mineral ore from which chromium is produced"
            },
            {
               "Result" : "<a href=\"http://duckduckgo.com/Ferrochrome\">Ferrochrome</a>, an alloy of chrome and iron, most commonly used in stainless steel production",
               "Icon" : {
                  "URL" : "https://i.duckduckgo.com/i/7d1f4f49.jpg",
                  "Height" : "",
                  "Width" : ""
               },
               "FirstURL" : "http://duckduckgo.com/Ferrochrome",
               "Text" : "Ferrochrome, an alloy of chrome and iron, most commonly used in stainless steel production"
            },
            {
               "Result" : "<a href=\"http://duckduckgo.com/Chromeffects\">Chromeffects</a>, a 3D graphics and video add-on for Windows 98",
               "Icon" : {
                  "URL" : "",
                  "Height" : "",
                  "Width" : ""
               },
               "FirstURL" : "http://duckduckgo.com/Chromeffects",
               "Text" : "Chromeffects, a 3D graphics and video add-on for Windows 98"
            },
            {
               "Result" : "<a href=\"http://duckduckgo.com/Chrome_alum\">Chrome alum</a>, a chemical used in mordanting and photographic film",
               "Icon" : {
                  "URL" : "https://i.duckduckgo.com/i/84b746e8.jpg",
                  "Height" : "",
                  "Width" : ""
               },
               "FirstURL" : "http://duckduckgo.com/Chrome_alum",
               "Text" : "Chrome alum, a chemical used in mordanting and photographic film"
            }
         ],
         "Name" : "See also"
      }
   ],
   "AbstractText" : "",
   "Abstract" : "",
   "AnswerType" : "",
   "Redirect" : "",
   "Type" : "D",
   "DefinitionURL" : "http://www.merriam-webster.com/dictionary/chrome",
   "Answer" : "",
   "Results" : [],
   "AbstractURL" : "https://en.wikipedia.org/wiki/Chrome"
})
print wrap_links(response)
