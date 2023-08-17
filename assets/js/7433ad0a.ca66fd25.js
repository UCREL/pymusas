"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[716],{3905:function(e,t,n){n.d(t,{Zo:function(){return u},kt:function(){return d}});var a=n(7294);function l(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function r(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,a)}return n}function i(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?r(Object(n),!0).forEach((function(t){l(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):r(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function o(e,t){if(null==e)return{};var n,a,l=function(e,t){if(null==e)return{};var n,a,l={},r=Object.keys(e);for(a=0;a<r.length;a++)n=r[a],t.indexOf(n)>=0||(l[n]=e[n]);return l}(e,t);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);for(a=0;a<r.length;a++)n=r[a],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(l[n]=e[n])}return l}var s=a.createContext({}),m=function(e){var t=a.useContext(s),n=t;return e&&(n="function"==typeof e?e(t):i(i({},t),e)),n},u=function(e){var t=m(e.components);return a.createElement(s.Provider,{value:t},e.children)},p={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},c=a.forwardRef((function(e,t){var n=e.components,l=e.mdxType,r=e.originalType,s=e.parentName,u=o(e,["components","mdxType","originalType","parentName"]),c=m(n),d=l,k=c["".concat(s,".").concat(d)]||c[d]||p[d]||r;return n?a.createElement(k,i(i({ref:t},u),{},{components:n})):a.createElement(k,i({ref:t},u))}));function d(e,t){var n=arguments,l=t&&t.mdxType;if("string"==typeof e||l){var r=n.length,i=new Array(r);i[0]=c;var o={};for(var s in t)hasOwnProperty.call(t,s)&&(o[s]=t[s]);o.originalType=e,o.mdxType="string"==typeof e?e:l,i[1]=o;for(var m=2;m<r;m++)i[m]=n[m];return a.createElement.apply(null,i)}return a.createElement.apply(null,n)}c.displayName="MDXCreateElement"},7968:function(e,t,n){n.r(t),n.d(t,{frontMatter:function(){return o},contentTitle:function(){return s},metadata:function(){return m},toc:function(){return u},default:function(){return c}});var a=n(3117),l=n(102),r=(n(7294),n(3905)),i=["components"],o={},s=void 0,m={unversionedId:"api/taggers/rules/single_word",id:"api/taggers/rules/single_word",title:"single_word",description:"pymusas.taggers.rules.single_word",source:"@site/docs/api/taggers/rules/single_word.md",sourceDirName:"api/taggers/rules",slug:"/api/taggers/rules/single_word",permalink:"/pymusas/api/taggers/rules/single_word",editUrl:"https://github.com/ucrel/pymusas/edit/main/docs/docs/api/taggers/rules/single_word.md",tags:[],version:"current",lastUpdatedBy:"Daisy Lal",lastUpdatedAt:1692311686,formattedLastUpdatedAt:"8/17/2023",frontMatter:{},sidebar:"api",previous:{title:"rule",permalink:"/pymusas/api/taggers/rules/rule"},next:{title:"util",permalink:"/pymusas/api/taggers/rules/util"}},u=[{value:"SingleWordRule",id:"singlewordrule",children:[{value:"__call__",id:"__call__",children:[],level:3},{value:"to_bytes",id:"to_bytes",children:[],level:3},{value:"from_bytes",id:"from_bytes",children:[],level:3},{value:"__eq__",id:"__eq__",children:[],level:3}],level:2}],p={toc:u};function c(e){var t=e.components,n=(0,l.Z)(e,i);return(0,r.kt)("wrapper",(0,a.Z)({},p,n,{components:t,mdxType:"MDXLayout"}),(0,r.kt)("div",{className:"source-div"},(0,r.kt)("p",null,(0,r.kt)("i",null,"pymusas"),(0,r.kt)("i",null,".taggers"),(0,r.kt)("i",null,".rules"),(0,r.kt)("strong",null,".single_word")),(0,r.kt)("p",null,(0,r.kt)("a",{className:"sourcelink",href:"https://github.com/UCREL/pymusas/blob/main/pymusas/taggers/rules/single_word.py"},"[SOURCE]"))),(0,r.kt)("div",null),(0,r.kt)("hr",null),(0,r.kt)("a",{id:"pymusas.taggers.rules.single_word.SingleWordRule"}),(0,r.kt)("h2",{id:"singlewordrule"},"SingleWordRule"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"class SingleWordRule(Rule):\n | ...\n | def __init__(\n |     self,\n |     lexicon_collection: Dict[str, List[str]],\n |     lemma_lexicon_collection: Dict[str, List[str]],\n |     pos_mapper: Optional[Dict[str, List[str]]] = None\n | )\n")),(0,r.kt)("p",null,"A single word rule match, is a rule that matches on single word lexicon\nentries. Entires can be matched on:"),(0,r.kt)("ol",null,(0,r.kt)("li",{parentName:"ol"},"Token and the token's Part Of Speech (POS) tag, e.g. ",(0,r.kt)("inlineCode",{parentName:"li"},"driving|adj")),(0,r.kt)("li",{parentName:"ol"},"Lemma and the lemma's POS tag, e.g. ",(0,r.kt)("inlineCode",{parentName:"li"},"drive|adj")),(0,r.kt)("li",{parentName:"ol"},"Token, e.g. ",(0,r.kt)("inlineCode",{parentName:"li"},"driving")),(0,r.kt)("li",{parentName:"ol"},"Lemma, e.g. ",(0,r.kt)("inlineCode",{parentName:"li"},"drive"))),(0,r.kt)("p",null,"In all cases matches are found based on the original token/lemma and lower\ncased versions of the token/lemma. These matches are found through searching\nthe ",(0,r.kt)("inlineCode",{parentName:"p"},"lexicon_collection")," and ",(0,r.kt)("inlineCode",{parentName:"p"},"lemma_lexicon_collection")," attributes."),(0,r.kt)("h4",{id:"singlewordrule.parameters"},"Parameters",(0,r.kt)("a",{className:"headerlink",href:"#singlewordrule.parameters",title:"Permanent link"},"\xb6")),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("strong",{parentName:"li"},"lexicon","_","collection")," : ",(0,r.kt)("inlineCode",{parentName:"li"},"Dict[str, List[str]]")," ",(0,r.kt)("br",null),"\nThe data to create ",(0,r.kt)("inlineCode",{parentName:"li"},"lexicon_collection")," instance attribute. A\nDictionary where the keys are a combination of\nlemma/token and POS in the following format: ",(0,r.kt)("inlineCode",{parentName:"li"},"{lemma}|{POS}")," and the\nvalues are a list of associated semantic tags."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("strong",{parentName:"li"},"lemma","_","lexicon","_","collection")," : ",(0,r.kt)("inlineCode",{parentName:"li"},"Dict[str, List[str]]")," ",(0,r.kt)("br",null),"\nThe data to create ",(0,r.kt)("inlineCode",{parentName:"li"},"lemma_lexicon_collection")," instance attribute. A\nDictionary where the keys are either just a lemma/token\nin the following format: ",(0,r.kt)("inlineCode",{parentName:"li"},"{lemma}")," and the\nvalues are a list of associated semantic tags."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("strong",{parentName:"li"},"pos","_","mapper")," : ",(0,r.kt)("inlineCode",{parentName:"li"},"Dict[str, List[str]]"),", optional (default = ",(0,r.kt)("inlineCode",{parentName:"li"},"None"),") ",(0,r.kt)("br",null),"\nIf not ",(0,r.kt)("inlineCode",{parentName:"li"},"None"),", maps from the given token's POS tagset to the desired\nPOS tagset, whereby the mapping is a ",(0,r.kt)("inlineCode",{parentName:"li"},"List")," of tags, at the moment there\nis no preference order in this list of POS tags. The POS mapping is\nuseful in situtation whereby the token's POS tagset is different to\nthose used in the lexicons. ",(0,r.kt)("strong",{parentName:"li"},"Note")," the longer the ",(0,r.kt)("inlineCode",{parentName:"li"},"List[str]")," for\neach POS mapping the slower the tagger, a one to one mapping will have\nno speed impact on the tagger. A selection of POS mappers can be found in\n",(0,r.kt)("a",{parentName:"li",href:"/pymusas/api/pos_mapper"},(0,r.kt)("inlineCode",{parentName:"a"},"pymusas.pos_mapper")),".")),(0,r.kt)("h4",{id:"singlewordrule.instance_attributes"},"Instance Attributes",(0,r.kt)("a",{className:"headerlink",href:"#singlewordrule.instance_attributes",title:"Permanent link"},"\xb6")),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("strong",{parentName:"li"},"lexicon","_","collection")," : ",(0,r.kt)("inlineCode",{parentName:"li"},"pymusas.lexicon_collection.LexiconCollection")," ",(0,r.kt)("br",null),"\nA ",(0,r.kt)("a",{parentName:"li",href:"/pymusas/api/lexicon_collection/#lexiconcollection"},(0,r.kt)("inlineCode",{parentName:"a"},"pymusas.lexicon_collection.LexiconCollection"))," instance that\nhas been initialised using the ",(0,r.kt)("inlineCode",{parentName:"li"},"lexicon_collection")," parameter."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("strong",{parentName:"li"},"lemma","_","lexicon","_","collection")," : ",(0,r.kt)("inlineCode",{parentName:"li"},"pymusas.lexicon_collection.LexiconCollection")," ",(0,r.kt)("br",null),"\nA ",(0,r.kt)("a",{parentName:"li",href:"/pymusas/api/lexicon_collection/#lexiconcollection"},(0,r.kt)("inlineCode",{parentName:"a"},"pymusas.lexicon_collection.LexiconCollection"))," instance that\nhas been initialised using the ",(0,r.kt)("inlineCode",{parentName:"li"},"lemma_lexicon_collection")," parameter."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("strong",{parentName:"li"},"pos","_","mapper")," : ",(0,r.kt)("inlineCode",{parentName:"li"},"Dict[str, List[str]]"),", optional (default = ",(0,r.kt)("inlineCode",{parentName:"li"},"None"),") ",(0,r.kt)("br",null),"\nThe given ",(0,r.kt)("inlineCode",{parentName:"li"},"pos_mapper"),".")),(0,r.kt)("a",{id:"pymusas.taggers.rules.single_word.SingleWordRule.__call__"}),(0,r.kt)("h3",{id:"__call__"},"_","_","call","_","_"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"class SingleWordRule(Rule):\n | ...\n | def __call__(\n |     self,\n |     tokens: List[str],\n |     lemmas: List[str],\n |     pos_tags: List[str]\n | ) -> List[List[RankingMetaData]]\n")),(0,r.kt)("p",null,"Given the tokens, lemmas, and POS tags for each word in a text,\nit returns for each token a ",(0,r.kt)("inlineCode",{parentName:"p"},"List")," of rules matches defined by\nthe ",(0,r.kt)("a",{parentName:"p",href:"/pymusas/api/rankers/ranking_meta_data/#rankingmetadata"},(0,r.kt)("inlineCode",{parentName:"a"},"pymusas.rankers.ranking_meta_data.RankingMetaData")),"\nobject based on the rule matches stated in the class docstring above."),(0,r.kt)("h4",{id:"__call__.parameters"},"Parameters",(0,r.kt)("a",{className:"headerlink",href:"#__call__.parameters",title:"Permanent link"},"\xb6")),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("strong",{parentName:"li"},"tokens")," : ",(0,r.kt)("inlineCode",{parentName:"li"},"List[str]")," ",(0,r.kt)("br",null),"\nThe tokens that are within the text."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("strong",{parentName:"li"},"lemmas")," : ",(0,r.kt)("inlineCode",{parentName:"li"},"List[str]")," ",(0,r.kt)("br",null),"\nThe lemmas of the tokens."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("strong",{parentName:"li"},"pos","_","tags")," : ",(0,r.kt)("inlineCode",{parentName:"li"},"List[str]")," ",(0,r.kt)("br",null),"\nThe Part Of Speech tags of the tokens.")),(0,r.kt)("h4",{id:"__call__.returns"},"Returns",(0,r.kt)("a",{className:"headerlink",href:"#__call__.returns",title:"Permanent link"},"\xb6")),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"List[List[RankingMetaData]]")," ",(0,r.kt)("br",null))),(0,r.kt)("a",{id:"pymusas.taggers.rules.single_word.SingleWordRule.to_bytes"}),(0,r.kt)("h3",{id:"to_bytes"},"to","_","bytes"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"class SingleWordRule(Rule):\n | ...\n | def to_bytes() -> bytes\n")),(0,r.kt)("p",null,"Serialises the ",(0,r.kt)("a",{parentName:"p",href:"#singlewordrule"},(0,r.kt)("inlineCode",{parentName:"a"},"SingleWordRule"))," to a bytestring."),(0,r.kt)("h4",{id:"to_bytes.returns"},"Returns",(0,r.kt)("a",{className:"headerlink",href:"#to_bytes.returns",title:"Permanent link"},"\xb6")),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"bytes")," ",(0,r.kt)("br",null))),(0,r.kt)("a",{id:"pymusas.taggers.rules.single_word.SingleWordRule.from_bytes"}),(0,r.kt)("h3",{id:"from_bytes"},"from","_","bytes"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},'class SingleWordRule(Rule):\n | ...\n | @staticmethod\n | def from_bytes(bytes_data: bytes) -> "SingleWordRule"\n')),(0,r.kt)("p",null,"Loads ",(0,r.kt)("a",{parentName:"p",href:"#singlewordrule"},(0,r.kt)("inlineCode",{parentName:"a"},"SingleWordRule"))," from the given bytestring and returns it."),(0,r.kt)("h4",{id:"from_bytes.parameters"},"Parameters",(0,r.kt)("a",{className:"headerlink",href:"#from_bytes.parameters",title:"Permanent link"},"\xb6")),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("strong",{parentName:"li"},"bytes","_","data")," : ",(0,r.kt)("inlineCode",{parentName:"li"},"bytes")," ",(0,r.kt)("br",null),"\nThe bytestring to load.")),(0,r.kt)("h4",{id:"from_bytes.returns"},"Returns",(0,r.kt)("a",{className:"headerlink",href:"#from_bytes.returns",title:"Permanent link"},"\xb6")),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("a",{parentName:"li",href:"#singlewordrule"},(0,r.kt)("inlineCode",{parentName:"a"},"SingleWordRule"))," ",(0,r.kt)("br",null))),(0,r.kt)("a",{id:"pymusas.taggers.rules.single_word.SingleWordRule.__eq__"}),(0,r.kt)("h3",{id:"__eq__"},"_","_","eq","_","_"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"class SingleWordRule(Rule):\n | ...\n | def __eq__(other: object) -> bool\n")),(0,r.kt)("p",null,"Given another object to compare too it will return ",(0,r.kt)("inlineCode",{parentName:"p"},"True")," if the other\nobject is the same class and initialised using with the same argument\nvalues."),(0,r.kt)("h4",{id:"__eq__.parameters"},"Parameters",(0,r.kt)("a",{className:"headerlink",href:"#__eq__.parameters",title:"Permanent link"},"\xb6")),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("strong",{parentName:"li"},"other")," : ",(0,r.kt)("inlineCode",{parentName:"li"},"object")," ",(0,r.kt)("br",null),"\nThe object to compare too.")),(0,r.kt)("h4",{id:"__eq__.returns"},"Returns",(0,r.kt)("a",{className:"headerlink",href:"#__eq__.returns",title:"Permanent link"},"\xb6")),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"True")," ",(0,r.kt)("br",null))))}c.isMDXComponent=!0}}]);