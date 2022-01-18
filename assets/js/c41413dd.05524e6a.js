"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[533],{3905:function(e,t,n){n.d(t,{Zo:function(){return u},kt:function(){return m}});var r=n(7294);function a(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function o(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function i(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?o(Object(n),!0).forEach((function(t){a(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):o(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function c(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},o=Object.keys(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var l=r.createContext({}),s=function(e){var t=r.useContext(l),n=t;return e&&(n="function"==typeof e?e(t):i(i({},t),e)),n},u=function(e){var t=s(e.components);return r.createElement(l.Provider,{value:t},e.children)},p={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},d=r.forwardRef((function(e,t){var n=e.components,a=e.mdxType,o=e.originalType,l=e.parentName,u=c(e,["components","mdxType","originalType","parentName"]),d=s(n),m=a,f=d["".concat(l,".").concat(m)]||d[m]||p[m]||o;return n?r.createElement(f,i(i({ref:t},u),{},{components:n})):r.createElement(f,i({ref:t},u))}));function m(e,t){var n=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var o=n.length,i=new Array(o);i[0]=d;var c={};for(var l in t)hasOwnProperty.call(t,l)&&(c[l]=t[l]);c.originalType=e,c.mdxType="string"==typeof e?e:a,i[1]=c;for(var s=2;s<o;s++)i[s]=n[s];return r.createElement.apply(null,i)}return r.createElement.apply(null,n)}d.displayName="MDXCreateElement"},4094:function(e,t,n){n.r(t),n.d(t,{frontMatter:function(){return c},contentTitle:function(){return l},metadata:function(){return s},toc:function(){return u},default:function(){return d}});var r=n(3117),a=n(102),o=(n(7294),n(3905)),i=["components"],c={},l=void 0,s={unversionedId:"api/config",id:"api/config",title:"config",description:"pymusas.config",source:"@site/docs/api/config.md",sourceDirName:"api",slug:"/api/config",permalink:"/pymusas/api/config",editUrl:"https://github.com/ucrel/pymusas/edit/main/docs/docs/api/config.md",tags:[],version:"current",lastUpdatedBy:"Andrew Moore",lastUpdatedAt:1642503331,formattedLastUpdatedAt:"1/18/2022",frontMatter:{},sidebar:"api",next:{title:"file_utils",permalink:"/pymusas/api/file_utils"}},u=[{value:"DEFAULT_XDG_CACHE_HOME",id:"default_xdg_cache_home",children:[],level:4},{value:"XDG_CACHE_HOME",id:"xdg_cache_home",children:[],level:4},{value:"DEFAULT_PYMUSAS_CACHE_HOME",id:"default_pymusas_cache_home",children:[],level:4},{value:"PYMUSAS_CACHE_HOME",id:"pymusas_cache_home",children:[],level:4},{value:"LANG_LEXICON_RESOUCRE_MAPPER",id:"lang_lexicon_resoucre_mapper",children:[],level:4}],p={toc:u};function d(e){var t=e.components,n=(0,a.Z)(e,i);return(0,o.kt)("wrapper",(0,r.Z)({},p,n,{components:t,mdxType:"MDXLayout"}),(0,o.kt)("div",{className:"source-div"},(0,o.kt)("p",null,(0,o.kt)("i",null,"pymusas"),(0,o.kt)("strong",null,".config")),(0,o.kt)("p",null,(0,o.kt)("a",{className:"sourcelink",href:"https://github.com/UCREL/pymusas/blob/main/pymusas/config.py"},"[SOURCE]"))),(0,o.kt)("div",null),(0,o.kt)("hr",null),(0,o.kt)("p",null,"This module has various attributes, of which the most important of these\nare listed below:"),(0,o.kt)("h4",{id:"pymusas.config.attributes"},"Attributes",(0,o.kt)("a",{className:"headerlink",href:"#pymusas.config.attributes",title:"Permanent link"},"\xb6")),(0,o.kt)("ul",null,(0,o.kt)("li",{parentName:"ul"},(0,o.kt)("strong",{parentName:"li"},"PYMUSAS","_","CACHE","_","HOME")," : ",(0,o.kt)("inlineCode",{parentName:"li"},"str")," ",(0,o.kt)("br",null),"\nThe directory that by default we store any downloaded data too. This\nattribute by default is set to ",(0,o.kt)("inlineCode",{parentName:"li"},"~/.cache/pymusas"),". This attribute can be\nset through the ",(0,o.kt)("inlineCode",{parentName:"li"},"PYMUSAS_HOME")," environment variable.")),(0,o.kt)("p",null,"The creation of the ",(0,o.kt)("inlineCode",{parentName:"p"},"PYMUSAS_CACHE_HOME")," attribute and how to set a default value\nfor it came from the ",(0,o.kt)("a",{parentName:"p",href:"https://github.com/huggingface/datasets/blob/d488db2f64f312f88f72bbc57a09b7eddb329182/src/datasets/config.py#L130"},"HuggingFace Datasets codebase\n(reference to their code)"),"."),(0,o.kt)("a",{id:"pymusas.config.DEFAULT_XDG_CACHE_HOME"}),(0,o.kt)("h4",{id:"default_xdg_cache_home"},"DEFAULT","_","XDG","_","CACHE","_","HOME"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"DEFAULT_XDG_CACHE_HOME: str = os.path.join(os.path.expanduser('~'), '.cache')\n")),(0,o.kt)("a",{id:"pymusas.config.XDG_CACHE_HOME"}),(0,o.kt)("h4",{id:"xdg_cache_home"},"XDG","_","CACHE","_","HOME"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},'XDG_CACHE_HOME: str = os.getenv("XDG_CACHE_HOME", DEFAULT_XDG_CACHE_HOME)\n')),(0,o.kt)("a",{id:"pymusas.config.DEFAULT_PYMUSAS_CACHE_HOME"}),(0,o.kt)("h4",{id:"default_pymusas_cache_home"},"DEFAULT","_","PYMUSAS","_","CACHE","_","HOME"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},'DEFAULT_PYMUSAS_CACHE_HOME: str = os.path.join(XDG_CACHE_HOME, "pymusas")\n')),(0,o.kt)("a",{id:"pymusas.config.PYMUSAS_CACHE_HOME"}),(0,o.kt)("h4",{id:"pymusas_cache_home"},"PYMUSAS","_","CACHE","_","HOME"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},'PYMUSAS_CACHE_HOME: str = os.path.expanduser(os.getenv("PYMUSAS_HOME", DEFAULT_PYMUSAS_CACHE_HOME))\n')),(0,o.kt)("a",{id:"pymusas.config.LANG_LEXICON_RESOUCRE_MAPPER"}),(0,o.kt)("h4",{id:"lang_lexicon_resoucre_mapper"},"LANG","_","LEXICON","_","RESOUCRE","_","MAPPER"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-python"},"LANG_LEXICON_RESOUCRE_MAPPER = {\n    'fr': {'lexicon': 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/French/sem ...\n")))}d.isMDXComponent=!0}}]);