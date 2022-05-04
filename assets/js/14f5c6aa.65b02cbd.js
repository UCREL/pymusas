"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[639],{3905:function(e,n,t){t.d(n,{Zo:function(){return u},kt:function(){return d}});var r=t(7294);function i(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function a(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function l(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?a(Object(t),!0).forEach((function(n){i(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):a(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function o(e,n){if(null==e)return{};var t,r,i=function(e,n){if(null==e)return{};var t,r,i={},a=Object.keys(e);for(r=0;r<a.length;r++)t=a[r],n.indexOf(t)>=0||(i[t]=e[t]);return i}(e,n);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(r=0;r<a.length;r++)t=a[r],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(i[t]=e[t])}return i}var s=r.createContext({}),p=function(e){var n=r.useContext(s),t=n;return e&&(t="function"==typeof e?e(n):l(l({},n),e)),t},u=function(e){var n=p(e.components);return r.createElement(s.Provider,{value:n},e.children)},_={inlineCode:"code",wrapper:function(e){var n=e.children;return r.createElement(r.Fragment,{},n)}},c=r.forwardRef((function(e,n){var t=e.components,i=e.mdxType,a=e.originalType,s=e.parentName,u=o(e,["components","mdxType","originalType","parentName"]),c=p(t),d=i,m=c["".concat(s,".").concat(d)]||c[d]||_[d]||a;return t?r.createElement(m,l(l({ref:n},u),{},{components:t})):r.createElement(m,l({ref:n},u))}));function d(e,n){var t=arguments,i=n&&n.mdxType;if("string"==typeof e||i){var a=t.length,l=new Array(a);l[0]=c;var o={};for(var s in n)hasOwnProperty.call(n,s)&&(o[s]=n[s]);o.originalType=e,o.mdxType="string"==typeof e?e:i,l[1]=o;for(var p=2;p<a;p++)l[p]=t[p];return r.createElement.apply(null,l)}return r.createElement.apply(null,t)}c.displayName="MDXCreateElement"},6127:function(e,n,t){t.r(n),t.d(n,{frontMatter:function(){return o},contentTitle:function(){return s},metadata:function(){return p},toc:function(){return u},default:function(){return c}});var r=t(3117),i=t(102),a=(t(7294),t(3905)),l=["components"],o={},s=void 0,p={unversionedId:"api/utils",id:"api/utils",title:"utils",description:"pymusas.utils",source:"@site/docs/api/utils.md",sourceDirName:"api",slug:"/api/utils",permalink:"/pymusas/api/utils",editUrl:"https://github.com/ucrel/pymusas/edit/main/docs/docs/api/utils.md",tags:[],version:"current",lastUpdatedBy:"Andrew Moore",lastUpdatedAt:1651674780,formattedLastUpdatedAt:"5/4/2022",frontMatter:{},sidebar:"api",previous:{title:"pos_mapper",permalink:"/pymusas/api/pos_mapper"},next:{title:"lexical_match",permalink:"/pymusas/api/rankers/lexical_match"}},u=[{value:"token_pos_tags_in_lexicon_entry",id:"token_pos_tags_in_lexicon_entry",children:[],level:3},{value:"unique_pos_tags_in_lexicon_entry",id:"unique_pos_tags_in_lexicon_entry",children:[],level:3}],_={toc:u};function c(e){var n=e.components,t=(0,i.Z)(e,l);return(0,a.kt)("wrapper",(0,r.Z)({},_,t,{components:n,mdxType:"MDXLayout"}),(0,a.kt)("div",{className:"source-div"},(0,a.kt)("p",null,(0,a.kt)("i",null,"pymusas"),(0,a.kt)("strong",null,".utils")),(0,a.kt)("p",null,(0,a.kt)("a",{className:"sourcelink",href:"https://github.com/UCREL/pymusas/blob/main/pymusas/utils.py"},"[SOURCE]"))),(0,a.kt)("div",null),(0,a.kt)("hr",null),(0,a.kt)("a",{id:"pymusas.utils.token_pos_tags_in_lexicon_entry"}),(0,a.kt)("h3",{id:"token_pos_tags_in_lexicon_entry"},"token","_","pos","_","tags","_","in","_","lexicon","_","entry"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"def token_pos_tags_in_lexicon_entry(\n    lexicon_entry: str\n) -> Iterable[Tuple[str, str]]\n")),(0,a.kt)("p",null,"Yields the token and associated POS tag in the given ",(0,a.kt)("inlineCode",{parentName:"p"},"lexicon_entry"),"."),(0,a.kt)("h4",{id:"token_pos_tags_in_lexicon_entry.parameters"},"Parameters",(0,a.kt)("a",{className:"headerlink",href:"#token_pos_tags_in_lexicon_entry.parameters",title:"Permanent link"},"\xb6")),(0,a.kt)("ul",null,(0,a.kt)("li",{parentName:"ul"},(0,a.kt)("strong",{parentName:"li"},"lexicon","_","entry")," : ",(0,a.kt)("inlineCode",{parentName:"li"},"str")," ",(0,a.kt)("br",null),"\nEither a Multi Word Expression template or single word lexicon entry,\nwhich is a sequence of words/tokens and Part Of Speech (POS) tags\njoined together by an underscore and separated by a single whitespace,\ne.g. ",(0,a.kt)("inlineCode",{parentName:"li"},"word1_POS1 word2_POS2 word3_POS3"),". For a single word lexicon it\nwould be ",(0,a.kt)("inlineCode",{parentName:"li"},"word1_POS1"),".")),(0,a.kt)("h4",{id:"token_pos_tags_in_lexicon_entry.returns"},"Returns",(0,a.kt)("a",{className:"headerlink",href:"#token_pos_tags_in_lexicon_entry.returns",title:"Permanent link"},"\xb6")),(0,a.kt)("ul",null,(0,a.kt)("li",{parentName:"ul"},(0,a.kt)("inlineCode",{parentName:"li"},"Iterable[Tuple[str, str]]")," ",(0,a.kt)("br",null))),(0,a.kt)("h4",{id:"token_pos_tags_in_lexicon_entry.raises"},"Raises",(0,a.kt)("a",{className:"headerlink",href:"#token_pos_tags_in_lexicon_entry.raises",title:"Permanent link"},"\xb6")),(0,a.kt)("ul",null,(0,a.kt)("li",{parentName:"ul"},(0,a.kt)("inlineCode",{parentName:"li"},"ValueError")," ",(0,a.kt)("br",null),"\nIf the lexicon entry when split on whitespace and then split by ",(0,a.kt)("inlineCode",{parentName:"li"},"_"),"\ndoes not create a ",(0,a.kt)("inlineCode",{parentName:"li"},"Iterable[Tuple[str, str]]")," whereby the tuple contains\nthe ",(0,a.kt)("inlineCode",{parentName:"li"},"token text")," and it's associated ",(0,a.kt)("inlineCode",{parentName:"li"},"POS tag"),".")),(0,a.kt)("h4",{id:"token_pos_tags_in_lexicon_entry.examples"},"Examples",(0,a.kt)("a",{className:"headerlink",href:"#token_pos_tags_in_lexicon_entry.examples",title:"Permanent link"},"\xb6")),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"from pymusas.utils import token_pos_tags_in_lexicon_entry\nmwe_template = 'East_noun London_noun is_det great_adj'\nassert ([('East', 'noun'), ('London', 'noun'), ('is', 'det'), ('great', 'adj')]\n        == list(token_pos_tags_in_lexicon_entry(mwe_template)))\nsingle_word_lexicon = 'East_noun'\nassert ([('East', 'noun')]\n        == list(token_pos_tags_in_lexicon_entry(single_word_lexicon)))\n")),(0,a.kt)("a",{id:"pymusas.utils.unique_pos_tags_in_lexicon_entry"}),(0,a.kt)("h3",{id:"unique_pos_tags_in_lexicon_entry"},"unique","_","pos","_","tags","_","in","_","lexicon","_","entry"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"def unique_pos_tags_in_lexicon_entry(\n    lexicon_entry: str\n) -> Set[str]\n")),(0,a.kt)("p",null,"Returns the unique POS tag values in the given ",(0,a.kt)("inlineCode",{parentName:"p"},"lexicon_entry"),"."),(0,a.kt)("h4",{id:"unique_pos_tags_in_lexicon_entry.parameters"},"Parameters",(0,a.kt)("a",{className:"headerlink",href:"#unique_pos_tags_in_lexicon_entry.parameters",title:"Permanent link"},"\xb6")),(0,a.kt)("ul",null,(0,a.kt)("li",{parentName:"ul"},(0,a.kt)("strong",{parentName:"li"},"lexicon","_","entry")," : ",(0,a.kt)("inlineCode",{parentName:"li"},"str")," ",(0,a.kt)("br",null),"\nEither a Multi Word Expression template or single word lexicon entry,\nwhich is a sequence of words/tokens and Part Of Speech (POS) tags\njoined together by an underscore and separated by a single whitespace,\ne.g. ",(0,a.kt)("inlineCode",{parentName:"li"},"word1_POS1 word2_POS2 word3_POS3"),". For a single word lexicon it\nwould be ",(0,a.kt)("inlineCode",{parentName:"li"},"word1_POS1"),".")),(0,a.kt)("h4",{id:"unique_pos_tags_in_lexicon_entry.returns"},"Returns",(0,a.kt)("a",{className:"headerlink",href:"#unique_pos_tags_in_lexicon_entry.returns",title:"Permanent link"},"\xb6")),(0,a.kt)("ul",null,(0,a.kt)("li",{parentName:"ul"},(0,a.kt)("inlineCode",{parentName:"li"},"Set[str]")," ",(0,a.kt)("br",null))),(0,a.kt)("h4",{id:"unique_pos_tags_in_lexicon_entry.raises"},"Raises",(0,a.kt)("a",{className:"headerlink",href:"#unique_pos_tags_in_lexicon_entry.raises",title:"Permanent link"},"\xb6")),(0,a.kt)("ul",null,(0,a.kt)("li",{parentName:"ul"},(0,a.kt)("inlineCode",{parentName:"li"},"ValueError")," ",(0,a.kt)("br",null),"\nIf the lexicon entry when split on whitespace and then split by ",(0,a.kt)("inlineCode",{parentName:"li"},"_"),"\ndoes not create a ",(0,a.kt)("inlineCode",{parentName:"li"},"List[Tuple[str, str]]")," whereby the tuple contains\nthe ",(0,a.kt)("inlineCode",{parentName:"li"},"token text")," and it's associated ",(0,a.kt)("inlineCode",{parentName:"li"},"POS tag"),".")),(0,a.kt)("h4",{id:"unique_pos_tags_in_lexicon_entry.examples"},"Examples",(0,a.kt)("a",{className:"headerlink",href:"#unique_pos_tags_in_lexicon_entry.examples",title:"Permanent link"},"\xb6")),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-python"},"from pymusas.utils import unique_pos_tags_in_lexicon_entry\nmwe_template = 'East_noun London_noun is_det great_adj'\nassert ({'noun', 'adj', 'det'}\n        == unique_pos_tags_in_lexicon_entry(mwe_template))\nsingle_word_lexicon = 'East_noun'\nassert {'noun'} == unique_pos_tags_in_lexicon_entry(single_word_lexicon)\n")))}c.isMDXComponent=!0}}]);