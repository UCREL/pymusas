"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[525],{3905:function(e,t,n){n.d(t,{Zo:function(){return _},kt:function(){return m}});var r=n(7294);function a(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function s(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function p(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?s(Object(n),!0).forEach((function(t){a(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):s(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function i(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},s=Object.keys(e);for(r=0;r<s.length;r++)n=s[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var s=Object.getOwnPropertySymbols(e);for(r=0;r<s.length;r++)n=s[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var o=r.createContext({}),c=function(e){var t=r.useContext(o),n=t;return e&&(n="function"==typeof e?e(t):p(p({},t),e)),n},_=function(e){var t=c(e.components);return r.createElement(o.Provider,{value:t},e.children)},u={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},l=r.forwardRef((function(e,t){var n=e.components,a=e.mdxType,s=e.originalType,o=e.parentName,_=i(e,["components","mdxType","originalType","parentName"]),l=c(n),m=a,k=l["".concat(o,".").concat(m)]||l[m]||u[m]||s;return n?r.createElement(k,p(p({ref:t},_),{},{components:n})):r.createElement(k,p({ref:t},_))}));function m(e,t){var n=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var s=n.length,p=new Array(s);p[0]=l;var i={};for(var o in t)hasOwnProperty.call(t,o)&&(i[o]=t[o]);i.originalType=e,i.mdxType="string"==typeof e?e:a,p[1]=i;for(var c=2;c<s;c++)p[c]=n[c];return r.createElement.apply(null,p)}return r.createElement.apply(null,n)}l.displayName="MDXCreateElement"},3099:function(e,t,n){n.r(t),n.d(t,{frontMatter:function(){return i},contentTitle:function(){return o},metadata:function(){return c},toc:function(){return _},default:function(){return l}});var r=n(3117),a=n(102),s=(n(7294),n(3905)),p=["components"],i={},o=void 0,c={unversionedId:"api/spacy_api/pos_mapper",id:"api/spacy_api/pos_mapper",title:"pos_mapper",description:"pymusas.spacyapi.posmapper",source:"@site/docs/api/spacy_api/pos_mapper.md",sourceDirName:"api/spacy_api",slug:"/api/spacy_api/pos_mapper",permalink:"/pymusas/api/spacy_api/pos_mapper",editUrl:"https://github.com/ucrel/pymusas/edit/main/docs/docs/api/spacy_api/pos_mapper.md",tags:[],version:"current",lastUpdatedBy:"Daisy Lal",lastUpdatedAt:1692311686,formattedLastUpdatedAt:"8/17/2023",frontMatter:{},sidebar:"api",previous:{title:"lexicon_collection",permalink:"/pymusas/api/spacy_api/lexicon_collection"},next:{title:"rankers",permalink:"/pymusas/api/spacy_api/rankers"}},_=[{value:"upos_to_usas_core",id:"upos_to_usas_core",children:[],level:3},{value:"usas_core_to_upos",id:"usas_core_to_upos",children:[],level:3},{value:"penn_chinese_treebank_to_usas_core",id:"penn_chinese_treebank_to_usas_core",children:[],level:3},{value:"usas_core_to_penn_chinese_treebank",id:"usas_core_to_penn_chinese_treebank",children:[],level:3},{value:"basic_corcencc_to_usas_core",id:"basic_corcencc_to_usas_core",children:[],level:3},{value:"usas_core_to_basic_corcencc",id:"usas_core_to_basic_corcencc",children:[],level:3}],u={toc:_};function l(e){var t=e.components,n=(0,a.Z)(e,p);return(0,s.kt)("wrapper",(0,r.Z)({},u,n,{components:t,mdxType:"MDXLayout"}),(0,s.kt)("div",{className:"source-div"},(0,s.kt)("p",null,(0,s.kt)("i",null,"pymusas"),(0,s.kt)("i",null,".spacy_api"),(0,s.kt)("strong",null,".pos_mapper")),(0,s.kt)("p",null,(0,s.kt)("a",{className:"sourcelink",href:"https://github.com/UCREL/pymusas/blob/main/pymusas/spacy_api/pos_mapper.py"},"[SOURCE]"))),(0,s.kt)("div",null),(0,s.kt)("hr",null),(0,s.kt)("p",null,"spaCy registered functions for loading Part Of Speech (POS) mappings."),(0,s.kt)("a",{id:"pymusas.spacy_api.pos_mapper.upos_to_usas_core"}),(0,s.kt)("h3",{id:"upos_to_usas_core"},"upos","_","to","_","usas","_","core"),(0,s.kt)("pre",null,(0,s.kt)("code",{parentName:"pre",className:"language-python"},"@spacy.util.registry.misc('pymusas.pos_mapper.UPOS_TO_USAS_COREv1')\ndef upos_to_usas_core() -> Dict[str, List[str]]\n")),(0,s.kt)("p",null,(0,s.kt)("inlineCode",{parentName:"p"},"pymusas.pos_mapper.UPOS_TO_USAS_COREv1")," is a registered function under the\n",(0,s.kt)("inlineCode",{parentName:"p"},"@misc")," function register. It returns the\n",(0,s.kt)("a",{parentName:"p",href:"/pymusas/api/pos_mapper/#upos_to_usas_core"},(0,s.kt)("inlineCode",{parentName:"a"},"pymusas.pos_mapper.UPOS_TO_USAS_CORE"))," mapping."),(0,s.kt)("h4",{id:"upos_to_usas_core.returns"},"Returns",(0,s.kt)("a",{className:"headerlink",href:"#upos_to_usas_core.returns",title:"Permanent link"},"\xb6")),(0,s.kt)("ul",null,(0,s.kt)("li",{parentName:"ul"},(0,s.kt)("inlineCode",{parentName:"li"},"Dict[str, List[str]]")," ",(0,s.kt)("br",null))),(0,s.kt)("a",{id:"pymusas.spacy_api.pos_mapper.usas_core_to_upos"}),(0,s.kt)("h3",{id:"usas_core_to_upos"},"usas","_","core","_","to","_","upos"),(0,s.kt)("pre",null,(0,s.kt)("code",{parentName:"pre",className:"language-python"},"@spacy.util.registry.misc('pymusas.pos_mapper.USAS_CORE_TO_UPOSv1')\ndef usas_core_to_upos() -> Dict[str, List[str]]\n")),(0,s.kt)("p",null,(0,s.kt)("inlineCode",{parentName:"p"},"pymusas.pos_mapper.USAS_CORE_TO_UPOSv1")," is a registered function under the\n",(0,s.kt)("inlineCode",{parentName:"p"},"@misc")," function register. It returns the\n",(0,s.kt)("a",{parentName:"p",href:"/pymusas/api/pos_mapper/#usas_core_to_upos"},(0,s.kt)("inlineCode",{parentName:"a"},"pymusas.pos_mapper.USAS_CORE_TO_UPOS"))," mapping."),(0,s.kt)("h4",{id:"usas_core_to_upos.returns"},"Returns",(0,s.kt)("a",{className:"headerlink",href:"#usas_core_to_upos.returns",title:"Permanent link"},"\xb6")),(0,s.kt)("ul",null,(0,s.kt)("li",{parentName:"ul"},(0,s.kt)("inlineCode",{parentName:"li"},"Dict[str, List[str]]")," ",(0,s.kt)("br",null))),(0,s.kt)("a",{id:"pymusas.spacy_api.pos_mapper.penn_chinese_treebank_to_usas_core"}),(0,s.kt)("h3",{id:"penn_chinese_treebank_to_usas_core"},"penn","_","chinese","_","treebank","_","to","_","usas","_","core"),(0,s.kt)("pre",null,(0,s.kt)("code",{parentName:"pre",className:"language-python"},"@spacy.util.registry.misc('pymusas.pos_mapper.PENN_CHINESE_TREEBANK_TO_USAS_COREv1')\ndef penn_chinese_treebank_to_usas_core() -> Dict[str, List[str]]\n")),(0,s.kt)("p",null,(0,s.kt)("inlineCode",{parentName:"p"},"pymusas.pos_mapper.PENN_CHINESE_TREEBANK_TO_USAS_COREv1")," is a registered\nfunction under the ",(0,s.kt)("inlineCode",{parentName:"p"},"@misc")," function register. It returns the\n",(0,s.kt)("a",{parentName:"p",href:"/pymusas/api/pos_mapper/#penn_chinese_treebank_to_usas_core"},(0,s.kt)("inlineCode",{parentName:"a"},"pymusas.pos_mapper.PENN_CHINESE_TREEBANK_TO_USAS_CORE"))," mapping."),(0,s.kt)("h4",{id:"penn_chinese_treebank_to_usas_core.returns"},"Returns",(0,s.kt)("a",{className:"headerlink",href:"#penn_chinese_treebank_to_usas_core.returns",title:"Permanent link"},"\xb6")),(0,s.kt)("ul",null,(0,s.kt)("li",{parentName:"ul"},(0,s.kt)("inlineCode",{parentName:"li"},"Dict[str, List[str]]")," ",(0,s.kt)("br",null))),(0,s.kt)("a",{id:"pymusas.spacy_api.pos_mapper.usas_core_to_penn_chinese_treebank"}),(0,s.kt)("h3",{id:"usas_core_to_penn_chinese_treebank"},"usas","_","core","_","to","_","penn","_","chinese","_","treebank"),(0,s.kt)("pre",null,(0,s.kt)("code",{parentName:"pre",className:"language-python"},"@spacy.util.registry.misc('pymusas.pos_mapper.USAS_CORE_TO_PENN_CHINESE_TREEBANKv1')\ndef usas_core_to_penn_chinese_treebank() -> Dict[str, List[str]]\n")),(0,s.kt)("p",null,(0,s.kt)("inlineCode",{parentName:"p"},"pymusas.pos_mapper.USAS_CORE_TO_PENN_CHINESE_TREEBANKv1")," is a registered\nfunction under the ",(0,s.kt)("inlineCode",{parentName:"p"},"@misc")," function register. It returns the\n",(0,s.kt)("a",{parentName:"p",href:"/pymusas/api/pos_mapper/#usas_core_to_penn_chinese_treebank"},(0,s.kt)("inlineCode",{parentName:"a"},"pymusas.pos_mapper.USAS_CORE_TO_PENN_CHINESE_TREEBANK"))," mapping."),(0,s.kt)("h4",{id:"usas_core_to_penn_chinese_treebank.returns"},"Returns",(0,s.kt)("a",{className:"headerlink",href:"#usas_core_to_penn_chinese_treebank.returns",title:"Permanent link"},"\xb6")),(0,s.kt)("ul",null,(0,s.kt)("li",{parentName:"ul"},(0,s.kt)("inlineCode",{parentName:"li"},"Dict[str, List[str]]")," ",(0,s.kt)("br",null))),(0,s.kt)("a",{id:"pymusas.spacy_api.pos_mapper.basic_corcencc_to_usas_core"}),(0,s.kt)("h3",{id:"basic_corcencc_to_usas_core"},"basic","_","corcencc","_","to","_","usas","_","core"),(0,s.kt)("pre",null,(0,s.kt)("code",{parentName:"pre",className:"language-python"},"@spacy.util.registry.misc('pymusas.pos_mapper.BASIC_CORCENCC_TO_USAS_COREv1')\ndef basic_corcencc_to_usas_core() -> Dict[str, List[str]]\n")),(0,s.kt)("p",null,(0,s.kt)("inlineCode",{parentName:"p"},"pymusas.pos_mapper.BASIC_CORCENCC_TO_USAS_COREv1")," is a registered\nfunction under the ",(0,s.kt)("inlineCode",{parentName:"p"},"@misc")," function register. It returns the\n",(0,s.kt)("a",{parentName:"p",href:"/pymusas/api/pos_mapper/#basic_corcencc_to_usas_core"},(0,s.kt)("inlineCode",{parentName:"a"},"pymusas.pos_mapper.BASIC_CORCENCC_TO_USAS_CORE"))," mapping."),(0,s.kt)("h4",{id:"basic_corcencc_to_usas_core.returns"},"Returns",(0,s.kt)("a",{className:"headerlink",href:"#basic_corcencc_to_usas_core.returns",title:"Permanent link"},"\xb6")),(0,s.kt)("ul",null,(0,s.kt)("li",{parentName:"ul"},(0,s.kt)("inlineCode",{parentName:"li"},"Dict[str, List[str]]")," ",(0,s.kt)("br",null))),(0,s.kt)("a",{id:"pymusas.spacy_api.pos_mapper.usas_core_to_basic_corcencc"}),(0,s.kt)("h3",{id:"usas_core_to_basic_corcencc"},"usas","_","core","_","to","_","basic","_","corcencc"),(0,s.kt)("pre",null,(0,s.kt)("code",{parentName:"pre",className:"language-python"},"@spacy.util.registry.misc('pymusas.pos_mapper.USAS_CORE_TO_BASIC_CORCENCCv1')\ndef usas_core_to_basic_corcencc() -> Dict[str, List[str]]\n")),(0,s.kt)("p",null,(0,s.kt)("inlineCode",{parentName:"p"},"pymusas.pos_mapper.USAS_CORE_TO_BASIC_CORCENCCv1")," is a registered\nfunction under the ",(0,s.kt)("inlineCode",{parentName:"p"},"@misc")," function register. It returns the\n",(0,s.kt)("a",{parentName:"p",href:"/pymusas/api/pos_mapper/#usas_core_to_basic_corcencc"},(0,s.kt)("inlineCode",{parentName:"a"},"pymusas.pos_mapper.USAS_CORE_TO_BASIC_CORCENCC"))," mapping."),(0,s.kt)("h4",{id:"usas_core_to_basic_corcencc.returns"},"Returns",(0,s.kt)("a",{className:"headerlink",href:"#usas_core_to_basic_corcencc.returns",title:"Permanent link"},"\xb6")),(0,s.kt)("ul",null,(0,s.kt)("li",{parentName:"ul"},(0,s.kt)("inlineCode",{parentName:"li"},"Dict[str, List[str]]")," ",(0,s.kt)("br",null))))}l.isMDXComponent=!0}}]);