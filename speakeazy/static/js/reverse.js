this.Urls=(function(){var Urls={};var self={url_patterns:{}};var _get_url=function(url_pattern){return function(){var _arguments,index,url,url_arg,url_args,_i,_len,_ref,_ref_list,match_ref,provided_keys,build_kwargs;_arguments=arguments;_ref_list=self.url_patterns[url_pattern];if(arguments.length==1&&typeof(arguments[0])=="object"){var provided_keys_list=Object.keys(arguments[0]);provided_keys={};for(_i=0;_i<provided_keys_list.length;_i++)
provided_keys[provided_keys_list[_i]]=1;match_ref=function(ref)
{var _i;if(ref[1].length!=provided_keys_list.length)
return false;for(_i=0;_i<ref[1].length&&ref[1][_i]in provided_keys;_i++);return _i==ref[1].length;}
build_kwargs=function(keys){return _arguments[0];}}else{match_ref=function(ref)
{return ref[1].length==_arguments.length;}
build_kwargs=function(keys){var kwargs={};for(var i=0;i<keys.length;i++){kwargs[keys[i]]=_arguments[i];}
return kwargs;}}
for(_i=0;_i<_ref_list.length&&!match_ref(_ref_list[_i]);_i++);if(_i==_ref_list.length)
return null;_ref=_ref_list[_i];url=_ref[0],url_args=build_kwargs(_ref[1]);for(url_arg in url_args){url=url.replace("%("+url_arg+")s",url_args[url_arg]||'');}
return'/'+url;};};var name,pattern,self,url_patterns,_i,_len,_ref;url_patterns=[['groups:group:audience:delete',[['groups/g/%(group)s/audiences/delete/%(audience)s/',['group','audience',]]],],['groups:group:audience:list',[['groups/g/%(group)s/audiences/',['group',]]],],['groups:group:audience:update',[['groups/g/%(group)s/audiences/update/%(audience)s/',['group','audience',]]],],['groups:group:audience:view',[['groups/g/%(group)s/audiences/view/%(audience)s/',['group','audience',]]],],['groups:group:groupView',[['groups/g/%(group)s/',['group',]]],],['groups:group:invite:add',[['groups/g/%(group)s/invites/add/',['group',]]],],['groups:group:invite:delete',[['groups/g/%(group)s/invites/delete/%(invite)s/',['group','invite',]]],],['groups:group:invite:list',[['groups/g/%(group)s/invites/',['group',]]],],['groups:group:invite:update',[['groups/g/%(group)s/invites/update/%(invite)s/',['group','invite',]]],],['groups:group:invite:view',[['groups/g/%(group)s/invites/view/%(invite)s/',['group','invite',]]],],['groups:group:submission:delete',[['groups/g/%(group)s/submissions/delete/%(pk)s/',['group','pk',]]],],['groups:group:submission:list',[['groups/g/%(group)s/submissions/',['group',]]],],['groups:group:submission:view',[['groups/g/%(group)s/submissions/view/%(pk)s/',['group','pk',]]],],['groups:group:user:delete',[['groups/g/%(group)s/users/delete/%(user)s/',['group','user',]]],],['groups:group:user:list',[['groups/g/%(group)s/users/',['group',]]],],['groups:group:user:update',[['groups/g/%(group)s/users/update/%(user)s/',['group','user',]]],],['groups:group:user:view',[['groups/g/%(group)s/users/view/%(user)s/',['group','user',]]],],['groups:groupDashboard',[['groups/home',[]]],],['groups:groupList',[['groups/',[]]],],['groups:joinGroup',[['groups/join/',[]]],],['groups:join_group_link',[['groups/join/%(group)s/%(token)s/',['group','token',]]],],['groups:newGroup',[['groups/new/',[]]],],['projects:newProject',[['projects/new/',[]]],],['projects:project:projectView',[['projects/p/%(project)s/',['project',]]],],['projects:project:recordingView',[['projects/p/%(project)s/%(recording)s/',['project','recording',]]],],['projects:projectList',[['projects/',[]]],],['recordings:record',[['recordings/record/%(project)s/',['project',]]],],['recordings:recording:comments:create',[['recordings/r/%(type)s/%(key)s/comments/create/',['type','key',]]],],['recordings:recording:evaluations:create',[['recordings/r/%(type)s/%(key)s/evaluations/create/',['type','key',]]],],['recordings:recording:share:submission',[['recordings/r/%(type)s/%(key)s/share/submission/',['type','key',]]],],['recordings:recording:view',[['recordings/r/%(type)s/%(key)s/',['type','key',]]]]];self.url_patterns={};for(_i=0,_len=url_patterns.length;_i<_len;_i++){_ref=url_patterns[_i],name=_ref[0],pattern=_ref[1];self.url_patterns[name]=pattern;Urls[name]=_get_url(name);Urls[name.replace(/-/g,'_')]=_get_url(name);}
return Urls;})();