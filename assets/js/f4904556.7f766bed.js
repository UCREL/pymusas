"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[561],{3905:function(e,t,a){a.d(t,{Zo:function(){return p},kt:function(){return h}});var n=a(7294);function r(e,t,a){return t in e?Object.defineProperty(e,t,{value:a,enumerable:!0,configurable:!0,writable:!0}):e[t]=a,e}function l(e,t){var a=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),a.push.apply(a,n)}return a}function i(e){for(var t=1;t<arguments.length;t++){var a=null!=arguments[t]?arguments[t]:{};t%2?l(Object(a),!0).forEach((function(t){r(e,t,a[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(a)):l(Object(a)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(a,t))}))}return e}function c(e,t){if(null==e)return{};var a,n,r=function(e,t){if(null==e)return{};var a,n,r={},l=Object.keys(e);for(n=0;n<l.length;n++)a=l[n],t.indexOf(a)>=0||(r[a]=e[a]);return r}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(n=0;n<l.length;n++)a=l[n],t.indexOf(a)>=0||Object.prototype.propertyIsEnumerable.call(e,a)&&(r[a]=e[a])}return r}var o=n.createContext({}),s=function(e){var t=n.useContext(o),a=t;return e&&(a="function"==typeof e?e(t):i(i({},t),e)),a},p=function(e){var t=s(e.components);return n.createElement(o.Provider,{value:t},e.children)},u={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},m=n.forwardRef((function(e,t){var a=e.components,r=e.mdxType,l=e.originalType,o=e.parentName,p=c(e,["components","mdxType","originalType","parentName"]),m=s(a),h=r,k=m["".concat(o,".").concat(h)]||m[h]||u[h]||l;return a?n.createElement(k,i(i({ref:t},p),{},{components:a})):n.createElement(k,i({ref:t},p))}));function h(e,t){var a=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var l=a.length,i=new Array(l);i[0]=m;var c={};for(var o in t)hasOwnProperty.call(t,o)&&(c[o]=t[o]);c.originalType=e,c.mdxType="string"==typeof e?e:r,i[1]=c;for(var s=2;s<l;s++)i[s]=a[s];return n.createElement.apply(null,i)}return n.createElement.apply(null,a)}m.displayName="MDXCreateElement"},8383:function(e,t,a){a.r(t),a.d(t,{frontMatter:function(){return c},contentTitle:function(){return o},metadata:function(){return s},toc:function(){return p},default:function(){return m}});var n=a(3117),r=a(102),l=(a(7294),a(3905)),i=["components"],c={},o=void 0,s={unversionedId:"api/rankers/lexical_match",id:"api/rankers/lexical_match",title:"lexical_match",description:"pymusas.rankers.lexical_match",source:"@site/docs/api/rankers/lexical_match.md",sourceDirName:"api/rankers",slug:"/api/rankers/lexical_match",permalink:"/pymusas/api/rankers/lexical_match",editUrl:"https://github.com/ucrel/pymusas/edit/main/docs/docs/api/rankers/lexical_match.md",tags:[],version:"current",lastUpdatedBy:"Paul Rayson",lastUpdatedAt:1651672020,formattedLastUpdatedAt:"5/4/2022",frontMatter:{},sidebar:"api",previous:{title:"utils",permalink:"/pymusas/api/utils"},next:{title:"lexicon_entry",permalink:"/pymusas/api/rankers/lexicon_entry"}},p=[{value:"LexicalMatch",id:"lexicalmatch",children:[{value:"TOKEN",id:"token",children:[],level:4},{value:"LEMMA",id:"lemma",children:[],level:4},{value:"TOKEN_LOWER",id:"token_lower",children:[],level:4},{value:"LEMMA_LOWER",id:"lemma_lower",children:[],level:4},{value:"__repr__",id:"__repr__",children:[],level:3}],level:2}],u={toc:p};function m(e){var t=e.components,a=(0,r.Z)(e,i);return(0,l.kt)("wrapper",(0,n.Z)({},u,a,{components:t,mdxType:"MDXLayout"}),(0,l.kt)("div",{className:"source-div"},(0,l.kt)("p",null,(0,l.kt)("i",null,"pymusas"),(0,l.kt)("i",null,".rankers"),(0,l.kt)("strong",null,".lexical_match")),(0,l.kt)("p",null,(0,l.kt)("a",{className:"sourcelink",href:"https://github.com/UCREL/pymusas/blob/main/pymusas/rankers/lexical_match.py"},"[SOURCE]"))),(0,l.kt)("div",null),(0,l.kt)("hr",null),(0,l.kt)("a",{id:"pymusas.rankers.lexical_match.LexicalMatch"}),(0,l.kt)("h2",{id:"lexicalmatch"},"LexicalMatch"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"class LexicalMatch(IntEnum)\n")),(0,l.kt)("p",null,"Descriptions of the lexical matches and their ordering in tagging priority\nduring ranking. Lower the value and rank the higher the tagging priority."),(0,l.kt)("p",null,"The ",(0,l.kt)("inlineCode",{parentName:"p"},"value")," attribute of each instance attribute is of type ",(0,l.kt)("inlineCode",{parentName:"p"},"int"),". For the\nbest explanation see the example below."),(0,l.kt)("h4",{id:"lexicalmatch.instance_attributes"},"Instance Attributes",(0,l.kt)("a",{className:"headerlink",href:"#lexicalmatch.instance_attributes",title:"Permanent link"},"\xb6")),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("strong",{parentName:"li"},"TOKEN")," : ",(0,l.kt)("inlineCode",{parentName:"li"},"int")," ",(0,l.kt)("br",null),"\nThe lexicon entry matched on the token text."),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("strong",{parentName:"li"},"LEMMA")," : ",(0,l.kt)("inlineCode",{parentName:"li"},"int")," ",(0,l.kt)("br",null),"\nThe lexicon entry matched on the lemma of the token."),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("strong",{parentName:"li"},"TOKEN","_","LOWER")," : ",(0,l.kt)("inlineCode",{parentName:"li"},"int")," ",(0,l.kt)("br",null),"\nThe lexicon entry matched on the lower cased token text."),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("strong",{parentName:"li"},"LEMMA","_","LOWER")," : ",(0,l.kt)("inlineCode",{parentName:"li"},"int")," ",(0,l.kt)("br",null),"\nThe lexicon entry matched on the lower cased lemma of the token.")),(0,l.kt)("h4",{id:"lexicalmatch.examples"},"Examples",(0,l.kt)("a",{className:"headerlink",href:"#lexicalmatch.examples",title:"Permanent link"},"\xb6")),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"from pymusas.rankers.lexical_match import LexicalMatch\nassert 1 == LexicalMatch.TOKEN\nassert 'TOKEN' == LexicalMatch.TOKEN.name\nassert 1 == LexicalMatch.TOKEN.value\n\nassert 2 == LexicalMatch.LEMMA\nassert 3 == LexicalMatch.TOKEN_LOWER\nassert 4 == LexicalMatch.LEMMA_LOWER\n\nassert 2 < LexicalMatch.LEMMA_LOWER\n")),(0,l.kt)("a",{id:"pymusas.rankers.lexical_match.LexicalMatch.TOKEN"}),(0,l.kt)("h4",{id:"token"},"TOKEN"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"class LexicalMatch(IntEnum):\n | ...\n | TOKEN = 1\n")),(0,l.kt)("a",{id:"pymusas.rankers.lexical_match.LexicalMatch.LEMMA"}),(0,l.kt)("h4",{id:"lemma"},"LEMMA"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"class LexicalMatch(IntEnum):\n | ...\n | LEMMA = 2\n")),(0,l.kt)("a",{id:"pymusas.rankers.lexical_match.LexicalMatch.TOKEN_LOWER"}),(0,l.kt)("h4",{id:"token_lower"},"TOKEN","_","LOWER"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"class LexicalMatch(IntEnum):\n | ...\n | TOKEN_LOWER = 3\n")),(0,l.kt)("a",{id:"pymusas.rankers.lexical_match.LexicalMatch.LEMMA_LOWER"}),(0,l.kt)("h4",{id:"lemma_lower"},"LEMMA","_","LOWER"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"class LexicalMatch(IntEnum):\n | ...\n | LEMMA_LOWER = 4\n")),(0,l.kt)("a",{id:"pymusas.rankers.lexical_match.LexicalMatch.__repr__"}),(0,l.kt)("h3",{id:"__repr__"},"_","_","repr","_","_"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"class LexicalMatch(IntEnum):\n | ...\n | def __repr__() -> str\n")),(0,l.kt)("p",null,"Machine readable string. When printed and run ",(0,l.kt)("inlineCode",{parentName:"p"},"eval()")," over the string\nyou should be able to recreate the object."))}m.isMDXComponent=!0}}]);