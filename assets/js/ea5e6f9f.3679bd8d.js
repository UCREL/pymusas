"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[69],{3905:function(e,t,n){n.d(t,{Zo:function(){return u},kt:function(){return k}});var a=n(7294);function r(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function l(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,a)}return n}function i(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?l(Object(n),!0).forEach((function(t){r(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):l(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function s(e,t){if(null==e)return{};var n,a,r=function(e,t){if(null==e)return{};var n,a,r={},l=Object.keys(e);for(a=0;a<l.length;a++)n=l[a],t.indexOf(n)>=0||(r[n]=e[n]);return r}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(a=0;a<l.length;a++)n=l[a],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(r[n]=e[n])}return r}var o=a.createContext({}),m=function(e){var t=a.useContext(o),n=t;return e&&(n="function"==typeof e?e(t):i(i({},t),e)),n},u=function(e){var t=m(e.components);return a.createElement(o.Provider,{value:t},e.children)},p={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},c=a.forwardRef((function(e,t){var n=e.components,r=e.mdxType,l=e.originalType,o=e.parentName,u=s(e,["components","mdxType","originalType","parentName"]),c=m(n),k=r,d=c["".concat(o,".").concat(k)]||c[k]||p[k]||l;return n?a.createElement(d,i(i({ref:t},u),{},{components:n})):a.createElement(d,i({ref:t},u))}));function k(e,t){var n=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var l=n.length,i=new Array(l);i[0]=c;var s={};for(var o in t)hasOwnProperty.call(t,o)&&(s[o]=t[o]);s.originalType=e,s.mdxType="string"==typeof e?e:r,i[1]=s;for(var m=2;m<l;m++)i[m]=n[m];return a.createElement.apply(null,i)}return a.createElement.apply(null,n)}c.displayName="MDXCreateElement"},8673:function(e,t,n){n.r(t),n.d(t,{frontMatter:function(){return s},contentTitle:function(){return o},metadata:function(){return m},toc:function(){return u},default:function(){return c}});var a=n(3117),r=n(102),l=(n(7294),n(3905)),i=["components"],s={},o=void 0,m={unversionedId:"api/taggers/rules/mwe",id:"api/taggers/rules/mwe",title:"mwe",description:"pymusas.taggers.rules.mwe",source:"@site/docs/api/taggers/rules/mwe.md",sourceDirName:"api/taggers/rules",slug:"/api/taggers/rules/mwe",permalink:"/pymusas/api/taggers/rules/mwe",editUrl:"https://github.com/ucrel/pymusas/edit/main/docs/docs/api/taggers/rules/mwe.md",tags:[],version:"current",lastUpdatedBy:"Paul Rayson",lastUpdatedAt:1651672020,formattedLastUpdatedAt:"5/4/2022",frontMatter:{},sidebar:"api",previous:{title:"rule_based",permalink:"/pymusas/api/taggers/rule_based"},next:{title:"rule",permalink:"/pymusas/api/taggers/rules/rule"}},u=[{value:"MWERule",id:"mwerule",children:[{value:"__call__",id:"__call__",children:[],level:3},{value:"to_bytes",id:"to_bytes",children:[],level:3},{value:"from_bytes",id:"from_bytes",children:[],level:3},{value:"__eq__",id:"__eq__",children:[],level:3}],level:2}],p={toc:u};function c(e){var t=e.components,n=(0,r.Z)(e,i);return(0,l.kt)("wrapper",(0,a.Z)({},p,n,{components:t,mdxType:"MDXLayout"}),(0,l.kt)("div",{className:"source-div"},(0,l.kt)("p",null,(0,l.kt)("i",null,"pymusas"),(0,l.kt)("i",null,".taggers"),(0,l.kt)("i",null,".rules"),(0,l.kt)("strong",null,".mwe")),(0,l.kt)("p",null,(0,l.kt)("a",{className:"sourcelink",href:"https://github.com/UCREL/pymusas/blob/main/pymusas/taggers/rules/mwe.py"},"[SOURCE]"))),(0,l.kt)("div",null),(0,l.kt)("hr",null),(0,l.kt)("a",{id:"pymusas.taggers.rules.mwe.MWERule"}),(0,l.kt)("h2",{id:"mwerule"},"MWERule"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"class MWERule(Rule):\n | ...\n | def __init__(\n |     self,\n |     mwe_lexicon_lookup: Dict[str, List[str]],\n |     pos_mapper: Optional[Dict[str, List[str]]] = None\n | ) -> None\n")),(0,l.kt)("p",null,"A Multi Word Expression (MWE) rule match can be one of the following matches:"),(0,l.kt)("ol",null,(0,l.kt)("li",{parentName:"ol"},(0,l.kt)("inlineCode",{parentName:"li"},"MWE_NON_SPECIAL")," match - whereby the combined token/lemma and POS\nis found within the given MWE Lexicon Collection (",(0,l.kt)("inlineCode",{parentName:"li"},"self.mwe_lexicon_collection"),")."),(0,l.kt)("li",{parentName:"ol"},(0,l.kt)("inlineCode",{parentName:"li"},"MWE_WILDCARD")," match - whereby the combined token/lemma and POS matches\na wildcard MWE template that is within the MWE Lexicon Collection\n(",(0,l.kt)("inlineCode",{parentName:"li"},"self.mwe_lexicon_collection"),").")),(0,l.kt)("p",null,"All rule matches use the\n",(0,l.kt)("inlineCode",{parentName:"p"},"pymusas.lexicon_collection.MWELexiconCollection.mwe_match"),"\nmethod for matching. Matches are found based on the original token/lemma and\nlower cased versions of the token/lemma."),(0,l.kt)("h4",{id:"mwerule.parameters"},"Parameters",(0,l.kt)("a",{className:"headerlink",href:"#mwerule.parameters",title:"Permanent link"},"\xb6")),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("strong",{parentName:"li"},"mwe","_","lexicon","_","lookup")," : ",(0,l.kt)("inlineCode",{parentName:"li"},"Dict[str, List[str]]")," ",(0,l.kt)("br",null),"\nThe data to create ",(0,l.kt)("inlineCode",{parentName:"li"},"mwe_lexicon_collection")," instance attribute. A\nDictionary where the keys are MWE templates, of any\n",(0,l.kt)("a",{parentName:"li",href:"/pymusas/api/lexicon_collection/#lexicontype"},(0,l.kt)("inlineCode",{parentName:"a"},"pymusas.lexicon_collection.LexiconType")),",\nand the values are a list of associated semantic tags."),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("strong",{parentName:"li"},"pos","_","mapper")," : ",(0,l.kt)("inlineCode",{parentName:"li"},"Dict[str, List[str]]"),", optional (default = ",(0,l.kt)("inlineCode",{parentName:"li"},"None"),") ",(0,l.kt)("br",null),"\nIf not ",(0,l.kt)("inlineCode",{parentName:"li"},"None"),", maps from the ",(0,l.kt)("inlineCode",{parentName:"li"},"mwe_lexicon_lookup")," POS tagset to the\ndesired POS tagset,whereby the mapping is a ",(0,l.kt)("inlineCode",{parentName:"li"},"List")," of tags,\nat the moment there is no preference order in this list of POS tags.\n",(0,l.kt)("strong",{parentName:"li"},"Note")," the longer the ",(0,l.kt)("inlineCode",{parentName:"li"},"List[str]")," for\neach POS mapping the slower the tagger, a one to one mapping will have\nno speed impact on the tagger. A selection of POS mappers can be found in\n",(0,l.kt)("a",{parentName:"li",href:"/pymusas/api/pos_mapper"},(0,l.kt)("inlineCode",{parentName:"a"},"pymusas.pos_mapper")),".")),(0,l.kt)("h4",{id:"mwerule.instance_attributes"},"Instance Attributes",(0,l.kt)("a",{className:"headerlink",href:"#mwerule.instance_attributes",title:"Permanent link"},"\xb6")),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("strong",{parentName:"li"},"mwe","_","lexicon","_","collection")," : ",(0,l.kt)("inlineCode",{parentName:"li"},"pymusas.lexicon_collection.MWELexiconCollection")," ",(0,l.kt)("br",null),"\nA ",(0,l.kt)("a",{parentName:"li",href:"/pymusas/api/lexicon_collection/#mwelexiconcollection"},(0,l.kt)("inlineCode",{parentName:"a"},"pymusas.lexicon_collection.MWELexiconCollection"))," instance that\nhas been initialised using the ",(0,l.kt)("inlineCode",{parentName:"li"},"mwe_lexicon_lookup")," and ",(0,l.kt)("inlineCode",{parentName:"li"},"pos_mapper"),"\nparameters. This collection is used to find MWE rule matches.")),(0,l.kt)("a",{id:"pymusas.taggers.rules.mwe.MWERule.__call__"}),(0,l.kt)("h3",{id:"__call__"},"_","_","call","_","_"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"class MWERule(Rule):\n | ...\n | def __call__(\n |     self,\n |     tokens: List[str],\n |     lemmas: List[str],\n |     pos_tags: List[str]\n | ) -> List[List[RankingMetaData]]\n")),(0,l.kt)("p",null,"Given the tokens, lemmas, and POS tags for each word in a text,\nit returns for each token a ",(0,l.kt)("inlineCode",{parentName:"p"},"List")," of rules matches defined by\nthe ",(0,l.kt)("a",{parentName:"p",href:"/pymusas/api/rankers/ranking_meta_data/#rankingmetadata"},(0,l.kt)("inlineCode",{parentName:"a"},"pymusas.rankers.ranking_meta_data.RankingMetaData"))," object based on\nthe rule matches stated in the class docstring above."),(0,l.kt)("h4",{id:"__call__.parameters"},"Parameters",(0,l.kt)("a",{className:"headerlink",href:"#__call__.parameters",title:"Permanent link"},"\xb6")),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("strong",{parentName:"li"},"tokens")," : ",(0,l.kt)("inlineCode",{parentName:"li"},"List[str]")," ",(0,l.kt)("br",null),"\nThe tokens that are within the text."),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("strong",{parentName:"li"},"lemmas")," : ",(0,l.kt)("inlineCode",{parentName:"li"},"List[str]")," ",(0,l.kt)("br",null),"\nThe lemmas of the tokens."),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("strong",{parentName:"li"},"pos","_","tags")," : ",(0,l.kt)("inlineCode",{parentName:"li"},"List[str]")," ",(0,l.kt)("br",null),"\nThe Part Of Speech tags of the tokens.")),(0,l.kt)("h4",{id:"__call__.returns"},"Returns",(0,l.kt)("a",{className:"headerlink",href:"#__call__.returns",title:"Permanent link"},"\xb6")),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"List[List[RankingMetaData]]")," ",(0,l.kt)("br",null))),(0,l.kt)("a",{id:"pymusas.taggers.rules.mwe.MWERule.to_bytes"}),(0,l.kt)("h3",{id:"to_bytes"},"to","_","bytes"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"class MWERule(Rule):\n | ...\n | def to_bytes() -> bytes\n")),(0,l.kt)("p",null,"Serialises the ",(0,l.kt)("a",{parentName:"p",href:"#mwerule"},(0,l.kt)("inlineCode",{parentName:"a"},"MWERule"))," to a bytestring."),(0,l.kt)("h4",{id:"to_bytes.returns"},"Returns",(0,l.kt)("a",{className:"headerlink",href:"#to_bytes.returns",title:"Permanent link"},"\xb6")),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"bytes")," ",(0,l.kt)("br",null))),(0,l.kt)("a",{id:"pymusas.taggers.rules.mwe.MWERule.from_bytes"}),(0,l.kt)("h3",{id:"from_bytes"},"from","_","bytes"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},'class MWERule(Rule):\n | ...\n | @staticmethod\n | def from_bytes(bytes_data: bytes) -> "MWERule"\n')),(0,l.kt)("p",null,"Loads ",(0,l.kt)("a",{parentName:"p",href:"#mwerule"},(0,l.kt)("inlineCode",{parentName:"a"},"MWERule"))," from the given bytestring and returns it."),(0,l.kt)("h4",{id:"from_bytes.parameters"},"Parameters",(0,l.kt)("a",{className:"headerlink",href:"#from_bytes.parameters",title:"Permanent link"},"\xb6")),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("strong",{parentName:"li"},"bytes","_","data")," : ",(0,l.kt)("inlineCode",{parentName:"li"},"bytes")," ",(0,l.kt)("br",null),"\nThe bytestring to load.")),(0,l.kt)("h4",{id:"from_bytes.returns"},"Returns",(0,l.kt)("a",{className:"headerlink",href:"#from_bytes.returns",title:"Permanent link"},"\xb6")),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("a",{parentName:"li",href:"#mwerule"},(0,l.kt)("inlineCode",{parentName:"a"},"MWERule"))," ",(0,l.kt)("br",null))),(0,l.kt)("a",{id:"pymusas.taggers.rules.mwe.MWERule.__eq__"}),(0,l.kt)("h3",{id:"__eq__"},"_","_","eq","_","_"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"class MWERule(Rule):\n | ...\n | def __eq__(other: object) -> bool\n")),(0,l.kt)("p",null,"Given another object to compare too it will return ",(0,l.kt)("inlineCode",{parentName:"p"},"True")," if the other\nobject is the same class and initialised using with the same argument\nvalues."),(0,l.kt)("h4",{id:"__eq__.parameters"},"Parameters",(0,l.kt)("a",{className:"headerlink",href:"#__eq__.parameters",title:"Permanent link"},"\xb6")),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("strong",{parentName:"li"},"other")," : ",(0,l.kt)("inlineCode",{parentName:"li"},"object")," ",(0,l.kt)("br",null),"\nThe object to compare too.")),(0,l.kt)("h4",{id:"__eq__.returns"},"Returns",(0,l.kt)("a",{className:"headerlink",href:"#__eq__.returns",title:"Permanent link"},"\xb6")),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"True")," ",(0,l.kt)("br",null))))}c.isMDXComponent=!0}}]);