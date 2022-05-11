"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[448],{3905:function(e,t,a){a.d(t,{Zo:function(){return c},kt:function(){return p}});var s=a(7294);function r(e,t,a){return t in e?Object.defineProperty(e,t,{value:a,enumerable:!0,configurable:!0,writable:!0}):e[t]=a,e}function i(e,t){var a=Object.keys(e);if(Object.getOwnPropertySymbols){var s=Object.getOwnPropertySymbols(e);t&&(s=s.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),a.push.apply(a,s)}return a}function n(e){for(var t=1;t<arguments.length;t++){var a=null!=arguments[t]?arguments[t]:{};t%2?i(Object(a),!0).forEach((function(t){r(e,t,a[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(a)):i(Object(a)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(a,t))}))}return e}function l(e,t){if(null==e)return{};var a,s,r=function(e,t){if(null==e)return{};var a,s,r={},i=Object.keys(e);for(s=0;s<i.length;s++)a=i[s],t.indexOf(a)>=0||(r[a]=e[a]);return r}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(s=0;s<i.length;s++)a=i[s],t.indexOf(a)>=0||Object.prototype.propertyIsEnumerable.call(e,a)&&(r[a]=e[a])}return r}var o=s.createContext({}),b=function(e){var t=s.useContext(o),a=t;return e&&(a="function"==typeof e?e(t):n(n({},t),e)),a},c=function(e){var t=b(e.components);return s.createElement(o.Provider,{value:t},e.children)},m={inlineCode:"code",wrapper:function(e){var t=e.children;return s.createElement(s.Fragment,{},t)}},u=s.forwardRef((function(e,t){var a=e.components,r=e.mdxType,i=e.originalType,o=e.parentName,c=l(e,["components","mdxType","originalType","parentName"]),u=b(a),p=r,_=u["".concat(o,".").concat(p)]||u[p]||m[p]||i;return a?s.createElement(_,n(n({ref:t},c),{},{components:a})):s.createElement(_,n({ref:t},c))}));function p(e,t){var a=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var i=a.length,n=new Array(i);n[0]=u;var l={};for(var o in t)hasOwnProperty.call(t,o)&&(l[o]=t[o]);l.originalType=e,l.mdxType="string"==typeof e?e:r,n[1]=l;for(var b=2;b<i;b++)n[b]=a[b];return s.createElement.apply(null,n)}return s.createElement.apply(null,a)}u.displayName="MDXCreateElement"},7272:function(e,t,a){a.r(t),a.d(t,{frontMatter:function(){return l},contentTitle:function(){return o},metadata:function(){return b},toc:function(){return c},default:function(){return u}});var s=a(3117),r=a(102),i=(a(7294),a(3905)),n=["components"],l={},o=void 0,b={unversionedId:"api/base",id:"api/base",title:"base",description:"pymusas.base",source:"@site/docs/api/base.md",sourceDirName:"api",slug:"/api/base",permalink:"/pymusas/api/base",editUrl:"https://github.com/ucrel/pymusas/edit/main/docs/docs/api/base.md",tags:[],version:"current",lastUpdatedBy:"Andrew Moore",lastUpdatedAt:1652297470,formattedLastUpdatedAt:"5/11/2022",frontMatter:{},sidebar:"api",next:{title:"config",permalink:"/pymusas/api/config"}},c=[{value:"Serialise",id:"serialise",children:[{value:"to_bytes",id:"to_bytes",children:[],level:3},{value:"from_bytes",id:"from_bytes",children:[],level:3},{value:"serialise_object_to_bytes",id:"serialise_object_to_bytes",children:[],level:3},{value:"serialise_object_from_bytes",id:"serialise_object_from_bytes",children:[],level:3},{value:"serialise_object_list_to_bytes",id:"serialise_object_list_to_bytes",children:[],level:3},{value:"serialise_object_list_from_bytes",id:"serialise_object_list_from_bytes",children:[],level:3}],level:2}],m={toc:c};function u(e){var t=e.components,a=(0,r.Z)(e,n);return(0,i.kt)("wrapper",(0,s.Z)({},m,a,{components:t,mdxType:"MDXLayout"}),(0,i.kt)("div",{className:"source-div"},(0,i.kt)("p",null,(0,i.kt)("i",null,"pymusas"),(0,i.kt)("strong",null,".base")),(0,i.kt)("p",null,(0,i.kt)("a",{className:"sourcelink",href:"https://github.com/UCREL/pymusas/blob/main/pymusas/base.py"},"[SOURCE]"))),(0,i.kt)("div",null),(0,i.kt)("hr",null),(0,i.kt)("p",null,"Base classes for custom classes to inherit from."),(0,i.kt)("a",{id:"pymusas.base.Serialise"}),(0,i.kt)("h2",{id:"serialise"},"Serialise"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"class Serialise(ABC)\n")),(0,i.kt)("p",null,"An ",(0,i.kt)("strong",{parentName:"p"},"abstract class")," that defines the basic methods, ",(0,i.kt)("inlineCode",{parentName:"p"},"to_bytes"),", and\n",(0,i.kt)("inlineCode",{parentName:"p"},"from_bytes")," that is required for all ",(0,i.kt)("a",{parentName:"p",href:"#serialise"},(0,i.kt)("inlineCode",{parentName:"a"},"Serialise")),"s."),(0,i.kt)("a",{id:"pymusas.base.Serialise.to_bytes"}),(0,i.kt)("h3",{id:"to_bytes"},"to","_","bytes"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"class Serialise(ABC):\n | ...\n | @abstractmethod\n | def to_bytes() -> bytes\n")),(0,i.kt)("p",null,"Serialises the class to a bytestring."),(0,i.kt)("h4",{id:"to_bytes.returns"},"Returns",(0,i.kt)("a",{className:"headerlink",href:"#to_bytes.returns",title:"Permanent link"},"\xb6")),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"bytes")," ",(0,i.kt)("br",null))),(0,i.kt)("a",{id:"pymusas.base.Serialise.from_bytes"}),(0,i.kt)("h3",{id:"from_bytes"},"from","_","bytes"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},'class Serialise(ABC):\n | ...\n | @staticmethod\n | @abstractmethod\n | def from_bytes(bytes_data: bytes) -> "Serialise"\n')),(0,i.kt)("p",null,"Loads the class from the given bytestring and returns it."),(0,i.kt)("h4",{id:"from_bytes.parameters"},"Parameters",(0,i.kt)("a",{className:"headerlink",href:"#from_bytes.parameters",title:"Permanent link"},"\xb6")),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("strong",{parentName:"li"},"bytes","_","data")," : ",(0,i.kt)("inlineCode",{parentName:"li"},"bytes")," ",(0,i.kt)("br",null),"\nThe bytestring to load.")),(0,i.kt)("h4",{id:"from_bytes.returns"},"Returns",(0,i.kt)("a",{className:"headerlink",href:"#from_bytes.returns",title:"Permanent link"},"\xb6")),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("a",{parentName:"li",href:"#serialise"},(0,i.kt)("inlineCode",{parentName:"a"},"Serialise"))," ",(0,i.kt)("br",null))),(0,i.kt)("a",{id:"pymusas.base.Serialise.serialise_object_to_bytes"}),(0,i.kt)("h3",{id:"serialise_object_to_bytes"},"serialise","_","object","_","to","_","bytes"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},'class Serialise(ABC):\n | ...\n | @staticmethod\n | def serialise_object_to_bytes(\n |     serialise_object: "Serialise"\n | ) -> bytes\n')),(0,i.kt)("p",null,"Given a serialise object it will serialise it to a bytestring."),(0,i.kt)("p",null,"This function in comparison to calling ",(0,i.kt)("inlineCode",{parentName:"p"},"to_bytes")," on the serialise\nobject saves meta data about what class it is so that when loading the\nbytes data later on you will know which class saved the data, this\nwould not happen if you called ",(0,i.kt)("inlineCode",{parentName:"p"},"to_bytes")," on the custom object."),(0,i.kt)("h4",{id:"serialise_object_to_bytes.parameters"},"Parameters",(0,i.kt)("a",{className:"headerlink",href:"#serialise_object_to_bytes.parameters",title:"Permanent link"},"\xb6")),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("strong",{parentName:"li"},"serialise","_","object")," : ",(0,i.kt)("inlineCode",{parentName:"li"},"Serialise")," ",(0,i.kt)("br",null),"\nThe serialise object, of type ",(0,i.kt)("a",{parentName:"li",href:"#serialise"},(0,i.kt)("inlineCode",{parentName:"a"},"Serialise")),", to serialise.")),(0,i.kt)("h4",{id:"serialise_object_to_bytes.returns"},"Returns",(0,i.kt)("a",{className:"headerlink",href:"#serialise_object_to_bytes.returns",title:"Permanent link"},"\xb6")),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"bytes")," ",(0,i.kt)("br",null))),(0,i.kt)("a",{id:"pymusas.base.Serialise.serialise_object_from_bytes"}),(0,i.kt)("h3",{id:"serialise_object_from_bytes"},"serialise","_","object","_","from","_","bytes"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},'class Serialise(ABC):\n | ...\n | @staticmethod\n | def serialise_object_from_bytes(\n |     bytes_data: bytes\n | ) -> "Serialise"\n')),(0,i.kt)("p",null,"Loads the serialise object from the given bytestring and return it.\nThis is the inverse of function of ",(0,i.kt)("a",{parentName:"p",href:"#serialise_object_to_bytes"},(0,i.kt)("inlineCode",{parentName:"a"},"serialise_object_to_bytes")),"."),(0,i.kt)("h4",{id:"serialise_object_from_bytes.parameters"},"Parameters",(0,i.kt)("a",{className:"headerlink",href:"#serialise_object_from_bytes.parameters",title:"Permanent link"},"\xb6")),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("strong",{parentName:"li"},"bytes","_","data")," : ",(0,i.kt)("inlineCode",{parentName:"li"},"bytes")," ",(0,i.kt)("br",null),"\nThe bytestring to load.")),(0,i.kt)("h4",{id:"serialise_object_from_bytes.returns"},"Returns",(0,i.kt)("a",{className:"headerlink",href:"#serialise_object_from_bytes.returns",title:"Permanent link"},"\xb6")),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"Serialise")," ",(0,i.kt)("br",null))),(0,i.kt)("a",{id:"pymusas.base.Serialise.serialise_object_list_to_bytes"}),(0,i.kt)("h3",{id:"serialise_object_list_to_bytes"},"serialise","_","object","_","list","_","to","_","bytes"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},'class Serialise(ABC):\n | ...\n | @staticmethod\n | def serialise_object_list_to_bytes(\n |     serialise_objects: Iterable["Serialise"]\n | ) -> bytes\n')),(0,i.kt)("p",null,"Serialises an ",(0,i.kt)("inlineCode",{parentName:"p"},"Iterable")," of serialise objects in the same way as\n",(0,i.kt)("a",{parentName:"p",href:"#serialise_object_to_bytes"},(0,i.kt)("inlineCode",{parentName:"a"},"serialise_object_to_bytes")),"."),(0,i.kt)("h4",{id:"serialise_object_list_to_bytes.parameters"},"Parameters",(0,i.kt)("a",{className:"headerlink",href:"#serialise_object_list_to_bytes.parameters",title:"Permanent link"},"\xb6")),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("strong",{parentName:"li"},"serialise","_","objects")," : ",(0,i.kt)("inlineCode",{parentName:"li"},"Iterable[Serialise]")," ",(0,i.kt)("br",null),"\nThe serialise objects, of type ",(0,i.kt)("a",{parentName:"li",href:"#serialise"},(0,i.kt)("inlineCode",{parentName:"a"},"Serialise")),", to serialise.")),(0,i.kt)("h4",{id:"serialise_object_list_to_bytes.returns"},"Returns",(0,i.kt)("a",{className:"headerlink",href:"#serialise_object_list_to_bytes.returns",title:"Permanent link"},"\xb6")),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"bytes")," ",(0,i.kt)("br",null))),(0,i.kt)("a",{id:"pymusas.base.Serialise.serialise_object_list_from_bytes"}),(0,i.kt)("h3",{id:"serialise_object_list_from_bytes"},"serialise","_","object","_","list","_","from","_","bytes"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},'class Serialise(ABC):\n | ...\n | @staticmethod\n | def serialise_object_list_from_bytes(\n |     bytes_data: bytes\n | ) -> Iterable["Serialise"]\n')),(0,i.kt)("p",null,"Loads the serialise objects from the given bytestring and return them.\nThis is the inverse of function of\n",(0,i.kt)("a",{parentName:"p",href:"#serialise_object_list_to_bytes"},(0,i.kt)("inlineCode",{parentName:"a"},"serialise_object_list_to_bytes")),"."),(0,i.kt)("h4",{id:"serialise_object_list_from_bytes.parameters"},"Parameters",(0,i.kt)("a",{className:"headerlink",href:"#serialise_object_list_from_bytes.parameters",title:"Permanent link"},"\xb6")),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("strong",{parentName:"li"},"bytes","_","data")," : ",(0,i.kt)("inlineCode",{parentName:"li"},"bytes")," ",(0,i.kt)("br",null),"\nThe bytestring to load.")),(0,i.kt)("h4",{id:"serialise_object_list_from_bytes.returns"},"Returns",(0,i.kt)("a",{className:"headerlink",href:"#serialise_object_list_from_bytes.returns",title:"Permanent link"},"\xb6")),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"Iterable[Serialise]")," ",(0,i.kt)("br",null))))}u.isMDXComponent=!0}}]);