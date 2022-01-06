"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[43],{3905:function(e,t,a){a.d(t,{Zo:function(){return m},kt:function(){return k}});var n=a(7294);function r(e,t,a){return t in e?Object.defineProperty(e,t,{value:a,enumerable:!0,configurable:!0,writable:!0}):e[t]=a,e}function i(e,t){var a=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),a.push.apply(a,n)}return a}function l(e){for(var t=1;t<arguments.length;t++){var a=null!=arguments[t]?arguments[t]:{};t%2?i(Object(a),!0).forEach((function(t){r(e,t,a[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(a)):i(Object(a)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(a,t))}))}return e}function o(e,t){if(null==e)return{};var a,n,r=function(e,t){if(null==e)return{};var a,n,r={},i=Object.keys(e);for(n=0;n<i.length;n++)a=i[n],t.indexOf(a)>=0||(r[a]=e[a]);return r}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(n=0;n<i.length;n++)a=i[n],t.indexOf(a)>=0||Object.prototype.propertyIsEnumerable.call(e,a)&&(r[a]=e[a])}return r}var s=n.createContext({}),p=function(e){var t=n.useContext(s),a=t;return e&&(a="function"==typeof e?e(t):l(l({},t),e)),a},m=function(e){var t=p(e.components);return n.createElement(s.Provider,{value:t},e.children)},u={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},c=n.forwardRef((function(e,t){var a=e.components,r=e.mdxType,i=e.originalType,s=e.parentName,m=o(e,["components","mdxType","originalType","parentName"]),c=p(a),k=r,g=c["".concat(s,".").concat(k)]||c[k]||u[k]||i;return a?n.createElement(g,l(l({ref:t},m),{},{components:a})):n.createElement(g,l({ref:t},m))}));function k(e,t){var a=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var i=a.length,l=new Array(i);l[0]=c;var o={};for(var s in t)hasOwnProperty.call(t,s)&&(o[s]=t[s]);o.originalType=e,o.mdxType="string"==typeof e?e:r,l[1]=o;for(var p=2;p<i;p++)l[p]=a[p];return n.createElement.apply(null,l)}return n.createElement.apply(null,a)}c.displayName="MDXCreateElement"},9941:function(e,t,a){a.r(t),a.d(t,{frontMatter:function(){return o},contentTitle:function(){return s},metadata:function(){return p},toc:function(){return m},default:function(){return c}});var n=a(3117),r=a(102),i=(a(7294),a(3905)),l=["components"],o={},s=void 0,p={unversionedId:"api/taggers/rule_based",id:"api/taggers/rule_based",title:"rule_based",description:"pymusas.taggers.rule_based",source:"@site/docs/api/taggers/rule_based.md",sourceDirName:"api/taggers",slug:"/api/taggers/rule_based",permalink:"/pymusas/api/taggers/rule_based",editUrl:"https://github.com/ucrel/pymusas/edit/main/docs/docs/api/taggers/rule_based.md",tags:[],version:"current",lastUpdatedBy:"Andrew Moore",lastUpdatedAt:1641458423,formattedLastUpdatedAt:"1/6/2022",frontMatter:{},sidebar:"api",previous:{title:"pos_mapper",permalink:"/pymusas/api/pos_mapper"},next:{title:"rule_based",permalink:"/pymusas/api/spacy_api/taggers/rule_based"}},m=[{value:"USASRuleBasedTagger",id:"usasrulebasedtagger",children:[{value:"tag_token",id:"tag_token",children:[],level:3},{value:"tag_tokens",id:"tag_tokens",children:[],level:3}],level:2}],u={toc:m};function c(e){var t=e.components,a=(0,r.Z)(e,l);return(0,i.kt)("wrapper",(0,n.Z)({},u,a,{components:t,mdxType:"MDXLayout"}),(0,i.kt)("div",{className:"source-div"},(0,i.kt)("p",null,(0,i.kt)("i",null,"pymusas"),(0,i.kt)("i",null,".taggers"),(0,i.kt)("strong",null,".rule_based")),(0,i.kt)("p",null,(0,i.kt)("a",{className:"sourcelink",href:"https://github.com/UCREL/pymusas/blob/main/pymusas/taggers/rule_based.py"},"[SOURCE]"))),(0,i.kt)("div",null),(0,i.kt)("hr",null),(0,i.kt)("a",{id:"pymusas.taggers.rule_based.USASRuleBasedTagger"}),(0,i.kt)("h2",{id:"usasrulebasedtagger"},"USASRuleBasedTagger"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"class USASRuleBasedTagger:\n | ...\n | def __init__(\n |     self,\n |     lexicon_lookup: Optional[Dict[str, List[str]]] = None,\n |     lemma_lexicon_lookup: Optional[Dict[str, List[str]]] = None,\n |     pos_mapper: Optional[Dict[str, List[str]]] = None\n | ) -> None\n")),(0,i.kt)("p",null,"The USAS Rule Based Tagger is based around the\n",(0,i.kt)("a",{parentName:"p",href:"https://github.com/UCREL/Multilingual-USAS"},"USAS Semantic Lexicon(s)."),"\nThe Tagger uses two Lexicon like data structures, both in the format of\n",(0,i.kt)("inlineCode",{parentName:"p"},"Dict[str, List[str]]"),", this structure maps a lemma (with or without it's\nPart Of Speech (POS) ) to a ",(0,i.kt)("inlineCode",{parentName:"p"},"List")," of USAS semantic tags.\nThe first semantic tag in the ",(0,i.kt)("inlineCode",{parentName:"p"},"List")," of tags is the most likely tag."),(0,i.kt)("p",null,"The easiest way of producing the Lexicon like data structures is through\n",(0,i.kt)("a",{parentName:"p",href:"/pymusas/api/lexicon_collection/#from_tsv"},(0,i.kt)("inlineCode",{parentName:"a"},"pymusas.lexicon_collection.from_tsv")),"\nwhereby the TSV file path would be to a USAS Semantic Lexicon."),(0,i.kt)("p",null,"The optional POS mapper is used in this tagger when the POS tagset within\nthe lexicons does not match the tagset used by the POS model that has\nbeen applied to the text. For instance a lot of the\n",(0,i.kt)("a",{parentName:"p",href:"https://github.com/UCREL/Multilingual-USAS"},"USAS Semantic Lexicon(s)."),"\nuse the USAS core tagset which does not align with the Universal Part of Speech (UPOS)\ntagset that a lot of the ",(0,i.kt)("a",{parentName:"p",href:"https://spacy.io/usage/linguistic-features#pos-tagging"},"spaCy POS models"),"\nhave in common. Therefore, when using the UPOS tags from the spaCy POS model for tagging text using a USAS\nSemantic lexicon with this tagger a POS mapper is required to map UPOS to\nUSAS core tags. The POS mapper is expected to map from the tagset of the POS model\nto the tagset of the lexicons, whereby the mapping is a ",(0,i.kt)("inlineCode",{parentName:"p"},"List"),"\nof tags, the first tag in the list is assumed to be the most relevant\nand the last to be the least. Some pre-compiled Dictionaries can be found in\nthe ",(0,i.kt)("a",{parentName:"p",href:"/pymusas/api/pos_mapper"},(0,i.kt)("inlineCode",{parentName:"a"},"pymusas.pos_mapper"))," module, e.g. the UPOS to USAS core ",(0,i.kt)("a",{parentName:"p",href:"/pymusas/api/pos_mapper/#upos_to_usas_core"},(0,i.kt)("inlineCode",{parentName:"a"},"pymusas.pos_mapper.UPOS_TO_USAS_CORE"))),(0,i.kt)("p",null,"Using these lexicon lookups the following rules are applied to assign a\n",(0,i.kt)("inlineCode",{parentName:"p"},"List")," of USAS semantic tags from the lexicon lookups to the given tokens\nin the given text. The text given is assumed to have been tokenised,\nlemmatised, and POS tagged:"),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Rules:")),(0,i.kt)("ol",null,(0,i.kt)("li",{parentName:"ol"},(0,i.kt)("strong",{parentName:"li"},"If ",(0,i.kt)("inlineCode",{parentName:"strong"},"pos_mapper")," is not ",(0,i.kt)("inlineCode",{parentName:"strong"},"None")),", map the POS, from the POS model,\nto the first POS value in the ",(0,i.kt)("inlineCode",{parentName:"li"},"List")," from the ",(0,i.kt)("inlineCode",{parentName:"li"},"pos_mapper"),"s ",(0,i.kt)("inlineCode",{parentName:"li"},"Dict"),". ",(0,i.kt)("strong",{parentName:"li"},"If")," the\n",(0,i.kt)("inlineCode",{parentName:"li"},"pos_mapper")," cannot map the POS, from the POS model, go to step 9."),(0,i.kt)("li",{parentName:"ol"},"If ",(0,i.kt)("inlineCode",{parentName:"li"},"POS==punc")," label as ",(0,i.kt)("inlineCode",{parentName:"li"},"PUNCT")),(0,i.kt)("li",{parentName:"ol"},"Lookup token and POS tag"),(0,i.kt)("li",{parentName:"ol"},"Lookup lemma and POS tag"),(0,i.kt)("li",{parentName:"ol"},"Lookup lower case token and POS tag"),(0,i.kt)("li",{parentName:"ol"},"Lookup lower case lemma and POS tag"),(0,i.kt)("li",{parentName:"ol"},"if ",(0,i.kt)("inlineCode",{parentName:"li"},"POS==num")," label as ",(0,i.kt)("inlineCode",{parentName:"li"},"N1")),(0,i.kt)("li",{parentName:"ol"},(0,i.kt)("strong",{parentName:"li"},"If there is another POS value in the ",(0,i.kt)("inlineCode",{parentName:"strong"},"pos_mapper"))," go back to step 2\nwith this new POS value else carry on to step 9."),(0,i.kt)("li",{parentName:"ol"},"Lookup token with any POS tag and choose first entry in lexicon."),(0,i.kt)("li",{parentName:"ol"},"Lookup lemma with any POS tag and choose first entry in lexicon."),(0,i.kt)("li",{parentName:"ol"},"Lookup lower case token with any POS tag and choose first entry in lexicon."),(0,i.kt)("li",{parentName:"ol"},"Lookup lower case lemma with any POS tag and choose first entry in lexicon."),(0,i.kt)("li",{parentName:"ol"},"Label as ",(0,i.kt)("inlineCode",{parentName:"li"},"Z99"),", this is the unmatched semantic tag.")),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"NOTE")," this tagger has been designed to be flexible with the amount of\nresources avaliable, if you do not have a POS tagger then assign\nthe POS tag an empty string e.g. ",(0,i.kt)("inlineCode",{parentName:"p"},"''"),". If you do not have a lexicon with\nPOS information then ",(0,i.kt)("inlineCode",{parentName:"p"},"lexicon_lookup")," can be ",(0,i.kt)("inlineCode",{parentName:"p"},"None"),". However, the fewer\nresources avaliable, less rules, stated above, will be applied making the\ntagger less effective."),(0,i.kt)("h4",{id:"usasrulebasedtagger.parameters"},"Parameters",(0,i.kt)("a",{className:"headerlink",href:"#usasrulebasedtagger.parameters",title:"Permanent link"},"\xb6")),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("strong",{parentName:"li"},"lexicon","_","lookup")," : ",(0,i.kt)("inlineCode",{parentName:"li"},"Dict[str, List[str]]"),", optional (default = ",(0,i.kt)("inlineCode",{parentName:"li"},"None"),") ",(0,i.kt)("br",null),"\nThe lexicon data structure with both lemma and POS information mapped to\na ",(0,i.kt)("inlineCode",{parentName:"li"},"List")," of USAS semantic tags e.g. ",(0,i.kt)("inlineCode",{parentName:"li"},"{'car_noun': ['Z2', 'Z1']}")),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("strong",{parentName:"li"},"lemma","_","lexicon","_","lookup")," : ",(0,i.kt)("inlineCode",{parentName:"li"},"Dict[str, List[str]]"),", optional (default = ",(0,i.kt)("inlineCode",{parentName:"li"},"None"),") ",(0,i.kt)("br",null),"\nThe lexicon data structure with only lemma information mapped to\na ",(0,i.kt)("inlineCode",{parentName:"li"},"List")," of USAS semantic tags e.g. ",(0,i.kt)("inlineCode",{parentName:"li"},"{'car': ['Z2', 'Z1']}")),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("strong",{parentName:"li"},"pos","_","mapper")," : ",(0,i.kt)("inlineCode",{parentName:"li"},"Dict[str, List[str]]"),", optional (default = ",(0,i.kt)("inlineCode",{parentName:"li"},"None"),") ",(0,i.kt)("br",null),"\nIf not ",(0,i.kt)("inlineCode",{parentName:"li"},"None"),", maps from the POS model tagset to the lexicon data\nPOS tagset, whereby the mapping is a ",(0,i.kt)("inlineCode",{parentName:"li"},"List")," of tags, the first tag in\nthe list is assumed to be the most relevant and the last to be the least.")),(0,i.kt)("h4",{id:"usasrulebasedtagger.instance_attributes"},"Instance Attributes",(0,i.kt)("a",{className:"headerlink",href:"#usasrulebasedtagger.instance_attributes",title:"Permanent link"},"\xb6")),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("strong",{parentName:"li"},"lexicon","_","lookup")," : ",(0,i.kt)("inlineCode",{parentName:"li"},"Dict[str, List[str]]")," ",(0,i.kt)("br",null),"\nThe given ",(0,i.kt)("inlineCode",{parentName:"li"},"lexicon_lookup")," data, if that was ",(0,i.kt)("inlineCode",{parentName:"li"},"None")," then this becomes\nan empty dictionary e.g. ",(0,i.kt)("inlineCode",{parentName:"li"},"{}")),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("strong",{parentName:"li"},"lemma","_","lexicon","_","lookup")," : ",(0,i.kt)("inlineCode",{parentName:"li"},"Dict[str, List[str]]")," ",(0,i.kt)("br",null),"\nThe given ",(0,i.kt)("inlineCode",{parentName:"li"},"lemma_lexicon_lookup")," data, if that was ",(0,i.kt)("inlineCode",{parentName:"li"},"None")," then this\nbecomes an empty dictionary e.g. ",(0,i.kt)("inlineCode",{parentName:"li"},"{}")),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("strong",{parentName:"li"},"pos","_","mapper")," : ",(0,i.kt)("inlineCode",{parentName:"li"},"Dict[str, List[str]]"),", optional (default = ",(0,i.kt)("inlineCode",{parentName:"li"},"None"),") ",(0,i.kt)("br",null),"\nThe given ",(0,i.kt)("inlineCode",{parentName:"li"},"pos_mapper"),".")),(0,i.kt)("h4",{id:"usasrulebasedtagger.examples"},"Examples",(0,i.kt)("a",{className:"headerlink",href:"#usasrulebasedtagger.examples",title:"Permanent link"},"\xb6")),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"from pymusas.lexicon_collection import LexiconCollection\nfrom pymusas.taggers.rule_based import USASRuleBasedTagger\nwelsh_lexicon_url = 'https://raw.githubusercontent.com/apmoore1/Multilingual-USAS/master/Welsh/semantic_lexicon_cy.tsv'\nlexicon_lookup = LexiconCollection.from_tsv(welsh_lexicon_url, include_pos=True)\nlemma_lexicon_lookup = LexiconCollection.from_tsv(welsh_lexicon_url, include_pos=False)\ntagger = USASRuleBasedTagger(lexicon_lookup, lemma_lexicon_lookup)\n")),(0,i.kt)("a",{id:"pymusas.taggers.rule_based.USASRuleBasedTagger.tag_token"}),(0,i.kt)("h3",{id:"tag_token"},"tag","_","token"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"class USASRuleBasedTagger:\n | ...\n | def tag_token(token: Tuple[str, str, str]) -> List[str]\n")),(0,i.kt)("p",null,"Given a tokens with the relevant lingustic information it returns\na list of USAS semantic tags, tagged according\nto the tagger's rules (see the class's doc string for tagger's rules).\nThe first semantic tag in the ",(0,i.kt)("inlineCode",{parentName:"p"},"List")," of tags is the most likely tag."),(0,i.kt)("h4",{id:"tag_token.parameters"},"Parameters",(0,i.kt)("a",{className:"headerlink",href:"#tag_token.parameters",title:"Permanent link"},"\xb6")),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("strong",{parentName:"li"},"tokens")," : ",(0,i.kt)("inlineCode",{parentName:"li"},"List[Tuple[str, str, str]]")," ",(0,i.kt)("br",null),"\nEach tuple represents a token. The tuple must contain the\nfollowing lingustic information per token;",(0,i.kt)("ol",{parentName:"li"},(0,i.kt)("li",{parentName:"ol"},"Full text form e.g. ",(0,i.kt)("inlineCode",{parentName:"li"},"cars")),(0,i.kt)("li",{parentName:"ol"},"Lemma/base form e.g. ",(0,i.kt)("inlineCode",{parentName:"li"},"car")),(0,i.kt)("li",{parentName:"ol"},"Part Of Speech e.g. ",(0,i.kt)("inlineCode",{parentName:"li"},"Noun"))))),(0,i.kt)("h4",{id:"tag_token.returns"},"Returns",(0,i.kt)("a",{className:"headerlink",href:"#tag_token.returns",title:"Permanent link"},"\xb6")),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"List[str]")," ",(0,i.kt)("br",null))),(0,i.kt)("a",{id:"pymusas.taggers.rule_based.USASRuleBasedTagger.tag_tokens"}),(0,i.kt)("h3",{id:"tag_tokens"},"tag","_","tokens"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"class USASRuleBasedTagger:\n | ...\n | def tag_tokens(\n |     self,\n |     tokens: Iterable[Tuple[str, str, str]]\n | ) -> Iterator[List[str]]\n")),(0,i.kt)("p",null,"Given a list/iterable of tokens with the relevant lingustic\ninformation it returns for each token a list of USAS semantic\ntags, tagged according to the tagger's rules (see the class's doc string for\ntagger's rules). The first semantic tag in the ",(0,i.kt)("inlineCode",{parentName:"p"},"List")," of tags is the\nmost likely tag."),(0,i.kt)("h4",{id:"tag_tokens.parameters"},"Parameters",(0,i.kt)("a",{className:"headerlink",href:"#tag_tokens.parameters",title:"Permanent link"},"\xb6")),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("strong",{parentName:"li"},"tokens")," : ",(0,i.kt)("inlineCode",{parentName:"li"},"Iterable[Tuple[str, str, str]]")," ",(0,i.kt)("br",null),"\nEach tuple represents a token. The tuple must contain the\nfollowing lingustic information per token;",(0,i.kt)("ol",{parentName:"li"},(0,i.kt)("li",{parentName:"ol"},"Full text form e.g. ",(0,i.kt)("inlineCode",{parentName:"li"},"cars")),(0,i.kt)("li",{parentName:"ol"},"Lemma/base form e.g. ",(0,i.kt)("inlineCode",{parentName:"li"},"car")),(0,i.kt)("li",{parentName:"ol"},"Part Of Speech e.g. ",(0,i.kt)("inlineCode",{parentName:"li"},"Noun"))))),(0,i.kt)("h4",{id:"tag_tokens.returns"},"Returns",(0,i.kt)("a",{className:"headerlink",href:"#tag_tokens.returns",title:"Permanent link"},"\xb6")),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"Iterator[List[str]]")," ",(0,i.kt)("br",null))))}c.isMDXComponent=!0}}]);