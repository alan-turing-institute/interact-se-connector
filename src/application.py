enterprise_search_name
secret_key
content_type_name
document_icon_asset


"""
See https://developer.interactsoftware.com/docs/how-to-set-up-enterprise-search
"""
http://{your domain}/api/searchapp

http://{your domain}/api/searchapp/{appid}/document



"""
$templateJSON = "{
  ""Url"": ""file:" + $uncPath + "/{filepath}"",
  ""Id"": ""{id}"",
  ""Title"": ""{filename}"",
  ""IsPublic"": ""true"",
  ""Body"": ""{filename}"",
  ""summary"": ""{filename}"",
  ""Author"": ""{author}"",
}"




"""
record = {
    "url": None,
    "id": None,
    "title": None,
    "is_public": None,
    "body": None,
    "summary": None,
    "author": None
}

"""
CRUD methods


"""

# Create records


# Delete records

How to list existing `docimentid`s?

 HTTP DELETE verb.

http:///api/searchapp/1/document/{documentid}