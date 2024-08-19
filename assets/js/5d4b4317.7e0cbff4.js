"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[783],{3905:function(e,n,t){t.d(n,{Zo:function(){return m},kt:function(){return k}});var a=t(7294);function i(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function r(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);n&&(a=a.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,a)}return t}function l(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?r(Object(t),!0).forEach((function(n){i(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):r(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function o(e,n){if(null==e)return{};var t,a,i=function(e,n){if(null==e)return{};var t,a,i={},r=Object.keys(e);for(a=0;a<r.length;a++)t=r[a],n.indexOf(t)>=0||(i[t]=e[t]);return i}(e,n);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);for(a=0;a<r.length;a++)t=r[a],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(i[t]=e[t])}return i}var c=a.createContext({}),s=function(e){var n=a.useContext(c),t=n;return e&&(t="function"==typeof e?e(n):l(l({},n),e)),t},m=function(e){var n=s(e.components);return a.createElement(c.Provider,{value:n},e.children)},d={inlineCode:"code",wrapper:function(e){var n=e.children;return a.createElement(a.Fragment,{},n)}},p=a.forwardRef((function(e,n){var t=e.components,i=e.mdxType,r=e.originalType,c=e.parentName,m=o(e,["components","mdxType","originalType","parentName"]),p=s(t),k=i,u=p["".concat(c,".").concat(k)]||p[k]||d[k]||r;return t?a.createElement(u,l(l({ref:n},m),{},{components:t})):a.createElement(u,l({ref:n},m))}));function k(e,n){var t=arguments,i=n&&n.mdxType;if("string"==typeof e||i){var r=t.length,l=new Array(r);l[0]=p;var o={};for(var c in n)hasOwnProperty.call(n,c)&&(o[c]=n[c]);o.originalType=e,o.mdxType="string"==typeof e?e:i,l[1]=o;for(var s=2;s<r;s++)l[s]=t[s];return a.createElement.apply(null,l)}return a.createElement.apply(null,t)}p.displayName="MDXCreateElement"},4539:function(e,n,t){t.r(n),t.d(n,{frontMatter:function(){return o},contentTitle:function(){return c},metadata:function(){return s},toc:function(){return m},default:function(){return p}});var a=t(3117),i=t(102),r=(t(7294),t(3905)),l=["components"],o={},c=void 0,s={unversionedId:"api/rankers/ranking_meta_data",id:"api/rankers/ranking_meta_data",title:"ranking_meta_data",description:"pymusas.rankers.rankingmetadata",source:"@site/docs/api/rankers/ranking_meta_data.md",sourceDirName:"api/rankers",slug:"/api/rankers/ranking_meta_data",permalink:"/pymusas/api/rankers/ranking_meta_data",editUrl:"https://github.com/ucrel/pymusas/edit/main/docs/docs/api/rankers/ranking_meta_data.md",tags:[],version:"current",lastUpdatedBy:"Paul Rayson",lastUpdatedAt:1724054083,formattedLastUpdatedAt:"8/19/2024",frontMatter:{},sidebar:"api",previous:{title:"lexicon_entry",permalink:"/pymusas/api/rankers/lexicon_entry"},next:{title:"lexicon_collection",permalink:"/pymusas/api/spacy_api/lexicon_collection"}},m=[{value:"RankingMetaData",id:"rankingmetadata",children:[{value:"lexicon_type",id:"lexicon_type",children:[],level:4},{value:"lexicon_n_gram_length",id:"lexicon_n_gram_length",children:[],level:4},{value:"lexicon_wildcard_count",id:"lexicon_wildcard_count",children:[],level:4},{value:"exclude_pos_information",id:"exclude_pos_information",children:[],level:4},{value:"lexical_match",id:"lexical_match",children:[],level:4},{value:"token_match_start_index",id:"token_match_start_index",children:[],level:4},{value:"token_match_end_index",id:"token_match_end_index",children:[],level:4},{value:"lexicon_entry_match",id:"lexicon_entry_match",children:[],level:4},{value:"semantic_tags",id:"semantic_tags",children:[],level:4}],level:2}],d={toc:m};function p(e){var n=e.components,t=(0,i.Z)(e,l);return(0,r.kt)("wrapper",(0,a.Z)({},d,t,{components:n,mdxType:"MDXLayout"}),(0,r.kt)("div",{className:"source-div"},(0,r.kt)("p",null,(0,r.kt)("i",null,"pymusas"),(0,r.kt)("i",null,".rankers"),(0,r.kt)("strong",null,".ranking_meta_data")),(0,r.kt)("p",null,(0,r.kt)("a",{className:"sourcelink",href:"https://github.com/UCREL/pymusas/blob/main/pymusas/rankers/ranking_meta_data.py"},"[SOURCE]"))),(0,r.kt)("div",null),(0,r.kt)("hr",null),(0,r.kt)("a",{id:"pymusas.rankers.ranking_meta_data.RankingMetaData"}),(0,r.kt)("h2",{id:"rankingmetadata"},"RankingMetaData"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"@dataclass(init=True, repr=True, eq=True, order=False,\n           unsafe_hash=False, frozen=True)\nclass RankingMetaData\n")),(0,r.kt)("p",null,"A RankingMetaData object contains all of the meta data about a lexicon\nentry match during the tagging process. This meta data can then be used\nto determine the ranking of the match comapred to other matches within the\nsame text/sentence that is being tagged."),(0,r.kt)("h4",{id:"rankingmetadata.instance_attributes"},"Instance Attributes",(0,r.kt)("a",{className:"headerlink",href:"#rankingmetadata.instance_attributes",title:"Permanent link"},"\xb6")),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("strong",{parentName:"li"},"lexicon","_","type")," : ",(0,r.kt)("inlineCode",{parentName:"li"},"LexiconType")," ",(0,r.kt)("br",null),"\nType associated to the lexicon entry."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("strong",{parentName:"li"},"lexicon","_","n","_","gram","_","length")," : ",(0,r.kt)("inlineCode",{parentName:"li"},"int")," ",(0,r.kt)("br",null),"\nThe n-gram size of the lexicon entry, e.g. ",(0,r.kt)("inlineCode",{parentName:"li"},"*_noun boot*_noun")," will be\nof length 2 and all single word lexicon entries will be of length 1."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("strong",{parentName:"li"},"lexicon","_","wildcard","_","count")," : ",(0,r.kt)("inlineCode",{parentName:"li"},"int")," ",(0,r.kt)("br",null),"\nNumber of wildcards in the lexicon entry, e.g. ",(0,r.kt)("inlineCode",{parentName:"li"},"*_noun boot*_noun")," will\nbe 2 and ",(0,r.kt)("inlineCode",{parentName:"li"},"ski_noun boot_noun")," will be 0."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("strong",{parentName:"li"},"exclude","_","pos","_","information")," : ",(0,r.kt)("inlineCode",{parentName:"li"},"bool")," ",(0,r.kt)("br",null),"\nWhether the POS information was excluded in the match. This is only ",(0,r.kt)("inlineCode",{parentName:"li"},"True"),"\nwhen the match ignores the POS information for single word lexicon entries.\nThis is always ",(0,r.kt)("inlineCode",{parentName:"li"},"False")," when used in a Multi Word Expression (MWE) lexicon\nentry match."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("strong",{parentName:"li"},"lexical","_","match")," : ",(0,r.kt)("inlineCode",{parentName:"li"},"LexicalMatch")," ",(0,r.kt)("br",null),"\nWhat ",(0,r.kt)("a",{parentName:"li",href:"#lexicalmatch"},(0,r.kt)("inlineCode",{parentName:"a"},"LexicalMatch"))," the lexicon entry matched on."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("strong",{parentName:"li"},"token","_","match","_","start","_","index")," : ",(0,r.kt)("inlineCode",{parentName:"li"},"int")," ",(0,r.kt)("br",null),"\nIndex of the first token in the lexicon entry match."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("strong",{parentName:"li"},"token","_","match","_","end","_","index")," : ",(0,r.kt)("inlineCode",{parentName:"li"},"int")," ",(0,r.kt)("br",null),"\nIndex of the last token in the lexicon entry match."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("strong",{parentName:"li"},"lexicon","_","entry","_","match")," : ",(0,r.kt)("inlineCode",{parentName:"li"},"str")," ",(0,r.kt)("br",null),"\nThe lexicon entry match, which can be either a single word or MWE entry\nmatch. In the case for single word this could be ",(0,r.kt)("inlineCode",{parentName:"li"},"Car|noun")," and in the\ncase for a MWE it would be it's template, e.g. ",(0,r.kt)("inlineCode",{parentName:"li"},"snow_noun boots_noun"),"."),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("strong",{parentName:"li"},"semantic","_","tags")," : ",(0,r.kt)("inlineCode",{parentName:"li"},"Tuple[str, ...]")," ",(0,r.kt)("br",null),"\nThe semantic tags associated with the lexicon entry. The semantic tags\nare in rank order, the most likely tag is the first tag in the tuple.\nThe Tuple can be of variable length hence the ",(0,r.kt)("inlineCode",{parentName:"li"},"...")," in the\ntype annotation.")),(0,r.kt)("a",{id:"pymusas.rankers.ranking_meta_data.RankingMetaData.lexicon_type"}),(0,r.kt)("h4",{id:"lexicon_type"},"lexicon","_","type"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"class RankingMetaData:\n | ...\n | lexicon_type: LexiconType = None\n")),(0,r.kt)("a",{id:"pymusas.rankers.ranking_meta_data.RankingMetaData.lexicon_n_gram_length"}),(0,r.kt)("h4",{id:"lexicon_n_gram_length"},"lexicon","_","n","_","gram","_","length"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"class RankingMetaData:\n | ...\n | lexicon_n_gram_length: int = None\n")),(0,r.kt)("a",{id:"pymusas.rankers.ranking_meta_data.RankingMetaData.lexicon_wildcard_count"}),(0,r.kt)("h4",{id:"lexicon_wildcard_count"},"lexicon","_","wildcard","_","count"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"class RankingMetaData:\n | ...\n | lexicon_wildcard_count: int = None\n")),(0,r.kt)("a",{id:"pymusas.rankers.ranking_meta_data.RankingMetaData.exclude_pos_information"}),(0,r.kt)("h4",{id:"exclude_pos_information"},"exclude","_","pos","_","information"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"class RankingMetaData:\n | ...\n | exclude_pos_information: bool = None\n")),(0,r.kt)("a",{id:"pymusas.rankers.ranking_meta_data.RankingMetaData.lexical_match"}),(0,r.kt)("h4",{id:"lexical_match"},"lexical","_","match"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"class RankingMetaData:\n | ...\n | lexical_match: LexicalMatch = None\n")),(0,r.kt)("a",{id:"pymusas.rankers.ranking_meta_data.RankingMetaData.token_match_start_index"}),(0,r.kt)("h4",{id:"token_match_start_index"},"token","_","match","_","start","_","index"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"class RankingMetaData:\n | ...\n | token_match_start_index: int = None\n")),(0,r.kt)("a",{id:"pymusas.rankers.ranking_meta_data.RankingMetaData.token_match_end_index"}),(0,r.kt)("h4",{id:"token_match_end_index"},"token","_","match","_","end","_","index"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"class RankingMetaData:\n | ...\n | token_match_end_index: int = None\n")),(0,r.kt)("a",{id:"pymusas.rankers.ranking_meta_data.RankingMetaData.lexicon_entry_match"}),(0,r.kt)("h4",{id:"lexicon_entry_match"},"lexicon","_","entry","_","match"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"class RankingMetaData:\n | ...\n | lexicon_entry_match: str = None\n")),(0,r.kt)("a",{id:"pymusas.rankers.ranking_meta_data.RankingMetaData.semantic_tags"}),(0,r.kt)("h4",{id:"semantic_tags"},"semantic","_","tags"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"class RankingMetaData:\n | ...\n | semantic_tags: Tuple[str, ...] = None\n")))}p.isMDXComponent=!0}}]);