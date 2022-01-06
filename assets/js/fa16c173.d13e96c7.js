"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[221],{3905:function(e,t,a){a.d(t,{Zo:function(){return m},kt:function(){return k}});var n=a(7294);function r(e,t,a){return t in e?Object.defineProperty(e,t,{value:a,enumerable:!0,configurable:!0,writable:!0}):e[t]=a,e}function l(e,t){var a=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),a.push.apply(a,n)}return a}function i(e){for(var t=1;t<arguments.length;t++){var a=null!=arguments[t]?arguments[t]:{};t%2?l(Object(a),!0).forEach((function(t){r(e,t,a[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(a)):l(Object(a)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(a,t))}))}return e}function s(e,t){if(null==e)return{};var a,n,r=function(e,t){if(null==e)return{};var a,n,r={},l=Object.keys(e);for(n=0;n<l.length;n++)a=l[n],t.indexOf(a)>=0||(r[a]=e[a]);return r}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(n=0;n<l.length;n++)a=l[n],t.indexOf(a)>=0||Object.prototype.propertyIsEnumerable.call(e,a)&&(r[a]=e[a])}return r}var o=n.createContext({}),p=function(e){var t=n.useContext(o),a=t;return e&&(a="function"==typeof e?e(t):i(i({},t),e)),a},m=function(e){var t=p(e.components);return n.createElement(o.Provider,{value:t},e.children)},u={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},d=n.forwardRef((function(e,t){var a=e.components,r=e.mdxType,l=e.originalType,o=e.parentName,m=s(e,["components","mdxType","originalType","parentName"]),d=p(a),k=r,g=d["".concat(o,".").concat(k)]||d[k]||u[k]||l;return a?n.createElement(g,i(i({ref:t},m),{},{components:a})):n.createElement(g,i({ref:t},m))}));function k(e,t){var a=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var l=a.length,i=new Array(l);i[0]=d;var s={};for(var o in t)hasOwnProperty.call(t,o)&&(s[o]=t[o]);s.originalType=e,s.mdxType="string"==typeof e?e:r,i[1]=s;for(var p=2;p<l;p++)i[p]=a[p];return n.createElement.apply(null,i)}return n.createElement.apply(null,a)}d.displayName="MDXCreateElement"},5167:function(e,t,a){a.r(t),a.d(t,{frontMatter:function(){return s},contentTitle:function(){return o},metadata:function(){return p},toc:function(){return m},default:function(){return d}});var n=a(3117),r=a(102),l=(a(7294),a(3905)),i=["components"],s={},o=void 0,p={unversionedId:"api/spacy_api/taggers/rule_based",id:"api/spacy_api/taggers/rule_based",title:"rule_based",description:"pymusas.spacyapi.taggers.rulebased",source:"@site/docs/api/spacy_api/taggers/rule_based.md",sourceDirName:"api/spacy_api/taggers",slug:"/api/spacy_api/taggers/rule_based",permalink:"/pymusas/api/spacy_api/taggers/rule_based",editUrl:"https://github.com/ucrel/pymusas/edit/main/docs/docs/api/spacy_api/taggers/rule_based.md",tags:[],version:"current",lastUpdatedBy:"Andrew Moore",lastUpdatedAt:1641458423,formattedLastUpdatedAt:"1/6/2022",frontMatter:{},sidebar:"api",previous:{title:"rule_based",permalink:"/pymusas/api/taggers/rule_based"}},m=[{value:"USASRuleBasedTagger",id:"usasrulebasedtagger",children:[{value:"__call__",id:"__call__",children:[],level:3},{value:"to_bytes",id:"to_bytes",children:[],level:3},{value:"from_bytes",id:"from_bytes",children:[],level:3},{value:"to_disk",id:"to_disk",children:[],level:3},{value:"from_disk",id:"from_disk",children:[],level:3}],level:2}],u={toc:m};function d(e){var t=e.components,a=(0,r.Z)(e,i);return(0,l.kt)("wrapper",(0,n.Z)({},u,a,{components:t,mdxType:"MDXLayout"}),(0,l.kt)("div",{className:"source-div"},(0,l.kt)("p",null,(0,l.kt)("i",null,"pymusas"),(0,l.kt)("i",null,".spacy_api"),(0,l.kt)("i",null,".taggers"),(0,l.kt)("strong",null,".rule_based")),(0,l.kt)("p",null,(0,l.kt)("a",{className:"sourcelink",href:"https://github.com/UCREL/pymusas/blob/main/pymusas/spacy_api/taggers/rule_based.py"},"[SOURCE]"))),(0,l.kt)("div",null),(0,l.kt)("hr",null),(0,l.kt)("a",{id:"pymusas.spacy_api.taggers.rule_based.USASRuleBasedTagger"}),(0,l.kt)("h2",{id:"usasrulebasedtagger"},"USASRuleBasedTagger"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"class USASRuleBasedTagger:\n | ...\n | def __init__(\n |     self,\n |     usas_tags_token_attr: str = 'usas_tags',\n |     pos_attribute: str = 'pos_',\n |     lemma_attribute: str = 'lemma_'\n | ) -> None\n")),(0,l.kt)("p",null,(0,l.kt)("a",{parentName:"p",href:"https://spacy.io/usage/processing-pipelines"},"spaCy pipeline component"),"\nfor rule based USAS tagger."),(0,l.kt)("p",null,"This component allows you to add ",(0,l.kt)("a",{parentName:"p",href:"http://ucrel.lancs.ac.uk/usas/"},"USAS semantic tags"),"\nto each spaCy ",(0,l.kt)("a",{parentName:"p",href:"https://spacy.io/api/token"},"Token"),", whereby these USAS tags\nhave been predicted through the following ",(0,l.kt)("a",{parentName:"p",href:"#usasrulebasedtagger.rules"},"rules"),", all of these rules depend on\ntwo Lexicon like data structures, the ",(0,l.kt)("inlineCode",{parentName:"p"},"lexicon_lookup")," and the ",(0,l.kt)("inlineCode",{parentName:"p"},"lemma_lexicon_lookup"),".\nBoth of these lexicons are of type ",(0,l.kt)("inlineCode",{parentName:"p"},"Dict[str, List[str]]")," which map a lemma\n(with or without it's Part Of Speech (POS) ) to a ",(0,l.kt)("inlineCode",{parentName:"p"},"List")," of USAS tags. The\nfirst semantic tag in the ",(0,l.kt)("inlineCode",{parentName:"p"},"List")," of tags is the most likely tag."),(0,l.kt)("p",null,"Furthermore, the optional POS mapper, ",(0,l.kt)("inlineCode",{parentName:"p"},"pos_mapper"),", is used in this tagger when the POS tagset\nwithin the lexicons does not match the tagset used by the POS model, which has\npreceding this tagger in the spaCy pipeline. The POS mapper is expected to\nmap from the tagset of the POS model to the tagset of the lexicons, whereby the\nmapping is a one-to-many mapping. The first tag in the ",(0,l.kt)("inlineCode",{parentName:"p"},"List")," is assumed to be the\nmost relevant and the last to be the least. Some pre-compiled Dictionaries can be\nfound in the ",(0,l.kt)("a",{parentName:"p",href:"/pymusas/api/pos_mapper"},(0,l.kt)("inlineCode",{parentName:"a"},"pymusas.pos_mapper"))," module, e.g. the UPOS to USAS\ncore ",(0,l.kt)("a",{parentName:"p",href:"/pymusas/api/pos_mapper/#upos_to_usas_core"},(0,l.kt)("inlineCode",{parentName:"a"},"pymusas.pos_mapper.UPOS_TO_USAS_CORE")),"."),(0,l.kt)("h4",{id:"usasrulebasedtagger.rules"},"Rules",(0,l.kt)("a",{className:"headerlink",href:"#usasrulebasedtagger.rules",title:"Permanent link"},"\xb6")),(0,l.kt)("ol",null,(0,l.kt)("li",{parentName:"ol"},(0,l.kt)("strong",{parentName:"li"},"If ",(0,l.kt)("inlineCode",{parentName:"strong"},"pos_mapper")," is not ",(0,l.kt)("inlineCode",{parentName:"strong"},"None")),", map the POS, from the POS model,\nto the first POS value in the ",(0,l.kt)("inlineCode",{parentName:"li"},"List")," from the ",(0,l.kt)("inlineCode",{parentName:"li"},"pos_mapper"),"s ",(0,l.kt)("inlineCode",{parentName:"li"},"Dict"),". ",(0,l.kt)("strong",{parentName:"li"},"If")," the\n",(0,l.kt)("inlineCode",{parentName:"li"},"pos_mapper")," cannot map the POS, from the POS model, go to step 9."),(0,l.kt)("li",{parentName:"ol"},"If ",(0,l.kt)("inlineCode",{parentName:"li"},"POS==punc")," label as ",(0,l.kt)("inlineCode",{parentName:"li"},"PUNCT")),(0,l.kt)("li",{parentName:"ol"},"Lookup token and POS tag"),(0,l.kt)("li",{parentName:"ol"},"Lookup lemma and POS tag"),(0,l.kt)("li",{parentName:"ol"},"Lookup lower case token and POS tag"),(0,l.kt)("li",{parentName:"ol"},"Lookup lower case lemma and POS tag"),(0,l.kt)("li",{parentName:"ol"},"if ",(0,l.kt)("inlineCode",{parentName:"li"},"POS==num")," label as ",(0,l.kt)("inlineCode",{parentName:"li"},"N1")),(0,l.kt)("li",{parentName:"ol"},(0,l.kt)("strong",{parentName:"li"},"If there is another POS value in the ",(0,l.kt)("inlineCode",{parentName:"strong"},"pos_mapper"))," go back to step 2\nwith this new POS value else carry on to step 9."),(0,l.kt)("li",{parentName:"ol"},"Lookup token with any POS tag and choose first entry in lexicon."),(0,l.kt)("li",{parentName:"ol"},"Lookup lemma with any POS tag and choose first entry in lexicon."),(0,l.kt)("li",{parentName:"ol"},"Lookup lower case token with any POS tag and choose first entry in lexicon."),(0,l.kt)("li",{parentName:"ol"},"Lookup lower case lemma with any POS tag and choose first entry in lexicon."),(0,l.kt)("li",{parentName:"ol"},"Label as ",(0,l.kt)("inlineCode",{parentName:"li"},"Z99"),", this is the unmatched semantic tag.")),(0,l.kt)("p",null,(0,l.kt)("strong",{parentName:"p"},"NOTE")," this tagger has been designed to be flexible with the amount of\nresources avaliable, if you do not have a POS tagger in the spaCy pipeline\nit will not use POS information. If you do not have a lexicon file with\nPOS information then ",(0,l.kt)("inlineCode",{parentName:"p"},"lexicon_lookup")," will be an empty ",(0,l.kt)("inlineCode",{parentName:"p"},"Dict"),". However, the fewer\nresources avaliable, less rules, stated above, will be applied making the\ntagger less effective."),(0,l.kt)("h4",{id:"usasrulebasedtagger.assigned_attributes"},"Assigned Attributes",(0,l.kt)("a",{className:"headerlink",href:"#usasrulebasedtagger.assigned_attributes",title:"Permanent link"},"\xb6")),(0,l.kt)("p",null,"The component assigns the predicted USAS tags to each spaCy ",(0,l.kt)("a",{parentName:"p",href:"https://spacy.io/api/token"},"Token")," under\n",(0,l.kt)("inlineCode",{parentName:"p"},"Token._.usas_tags")," attribute by default, this can be changed with the\n",(0,l.kt)("inlineCode",{parentName:"p"},"usas_tags_token_attr")," parameter to another attribute of\nthe ",(0,l.kt)("inlineCode",{parentName:"p"},"Token._"),", e.g. if ",(0,l.kt)("inlineCode",{parentName:"p"},"usas_tags_token_attr=semantic_tags")," then the attribute\nthe USAS tags will be assigned to for each token will be ",(0,l.kt)("inlineCode",{parentName:"p"},"Token._.semantic_tags"),"."),(0,l.kt)("table",null,(0,l.kt)("thead",{parentName:"table"},(0,l.kt)("tr",{parentName:"thead"},(0,l.kt)("th",{parentName:"tr",align:null},"Location"),(0,l.kt)("th",{parentName:"tr",align:null},"Type"),(0,l.kt)("th",{parentName:"tr",align:null},"Value"))),(0,l.kt)("tbody",{parentName:"table"},(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:null},"Token._.usas_tags"),(0,l.kt)("td",{parentName:"tr",align:null},(0,l.kt)("inlineCode",{parentName:"td"},"List[str]")),(0,l.kt)("td",{parentName:"tr",align:null},"Prediced USAS tags, the first semantic tag in the List of tags is the most likely tag.")))),(0,l.kt)("h4",{id:"usasrulebasedtagger.config_and_implementation"},"Config and implementation",(0,l.kt)("a",{className:"headerlink",href:"#usasrulebasedtagger.config_and_implementation",title:"Permanent link"},"\xb6")),(0,l.kt)("p",null,"The default config is defined by the pipeline component factory and describes\nhow the component should be configured. You can override its settings via the ",(0,l.kt)("inlineCode",{parentName:"p"},"config"),"\nargument on ",(0,l.kt)("a",{parentName:"p",href:"https://spacy.io/api/language#add_pipe"},"nlp.add_pipe")," or in your\n",(0,l.kt)("a",{parentName:"p",href:"https://spacy.io/usage/training#config"},"config.cfg for training"),"."),(0,l.kt)("table",null,(0,l.kt)("thead",{parentName:"table"},(0,l.kt)("tr",{parentName:"thead"},(0,l.kt)("th",{parentName:"tr",align:null},"Setting"),(0,l.kt)("th",{parentName:"tr",align:null},"Description"))),(0,l.kt)("tbody",{parentName:"table"},(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:null},"usas_tags_token_attr"),(0,l.kt)("td",{parentName:"tr",align:null},"See parameters section below")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:null},"pos_attribute"),(0,l.kt)("td",{parentName:"tr",align:null},"See parameters section below")),(0,l.kt)("tr",{parentName:"tbody"},(0,l.kt)("td",{parentName:"tr",align:null},"lemma_attribute"),(0,l.kt)("td",{parentName:"tr",align:null},"See parameters section below")))),(0,l.kt)("h4",{id:"usasrulebasedtagger.parameters"},"Parameters",(0,l.kt)("a",{className:"headerlink",href:"#usasrulebasedtagger.parameters",title:"Permanent link"},"\xb6")),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},(0,l.kt)("strong",{parentName:"p"},"usas","_","tags","_","token","_","attr")," : ",(0,l.kt)("inlineCode",{parentName:"p"},"str"),", optional (default = ",(0,l.kt)("inlineCode",{parentName:"p"},"usas_tags"),") ",(0,l.kt)("br",null),"\nThe name of the attribute to assign the predicted USAS tags too under\nthe ",(0,l.kt)("inlineCode",{parentName:"p"},"Token._")," class.")),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},(0,l.kt)("strong",{parentName:"p"},"pos","_","attribute")," : ",(0,l.kt)("inlineCode",{parentName:"p"},"str"),", optional (default = ",(0,l.kt)("inlineCode",{parentName:"p"},"pos_"),") ",(0,l.kt)("br",null),"\nThe name of the attribute that the Part Of Speech (POS) tag is assigned too\nwithin the ",(0,l.kt)("inlineCode",{parentName:"p"},"Token")," class. The POS tag value that comes from this attribute\nhas to be of type ",(0,l.kt)("inlineCode",{parentName:"p"},"str"),". With the current default we take the POS tag\nfrom ",(0,l.kt)("inlineCode",{parentName:"p"},"Token.pos_"))),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},(0,l.kt)("strong",{parentName:"p"},"lemma","_","attribute")," : ",(0,l.kt)("inlineCode",{parentName:"p"},"str"),", optional (default = ",(0,l.kt)("inlineCode",{parentName:"p"},"lemma_"),") ",(0,l.kt)("br",null),"\nThe name of the attribute that the lemma is assigned too within the ",(0,l.kt)("inlineCode",{parentName:"p"},"Token"),"\nclass. The lemma value that comes from this attribute has to be of\ntype ",(0,l.kt)("inlineCode",{parentName:"p"},"str"),". With the current default we take the lemma from ",(0,l.kt)("inlineCode",{parentName:"p"},"Token.lemma_")))),(0,l.kt)("h4",{id:"usasrulebasedtagger.instance_attributes"},"Instance Attributes",(0,l.kt)("a",{className:"headerlink",href:"#usasrulebasedtagger.instance_attributes",title:"Permanent link"},"\xb6")),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},(0,l.kt)("strong",{parentName:"p"},"usas","_","tags","_","token","_","attr")," : ",(0,l.kt)("inlineCode",{parentName:"p"},"str"),", optional (default = ",(0,l.kt)("inlineCode",{parentName:"p"},"usas_tags"),") ",(0,l.kt)("br",null))),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},(0,l.kt)("strong",{parentName:"p"},"pos","_","attribute")," : ",(0,l.kt)("inlineCode",{parentName:"p"},"str"),", optional (default = ",(0,l.kt)("inlineCode",{parentName:"p"},"pos_"),") ",(0,l.kt)("br",null))),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},(0,l.kt)("strong",{parentName:"p"},"lemma","_","attribute")," : ",(0,l.kt)("inlineCode",{parentName:"p"},"str"),", optional (default = ",(0,l.kt)("inlineCode",{parentName:"p"},"lemma_"),") ",(0,l.kt)("br",null))),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},(0,l.kt)("strong",{parentName:"p"},"lexicon","_","lookup")," : ",(0,l.kt)("inlineCode",{parentName:"p"},"Dict[str, List[str]]")," ",(0,l.kt)("br",null),"\nThe lexicon data structure with both lemma and POS information mapped\nto a ",(0,l.kt)("inlineCode",{parentName:"p"},"List")," of USAS semantic tags e.g. ",(0,l.kt)("inlineCode",{parentName:"p"},"{'Car|noun': ['Z2', 'Z1']}"),".\nBy default this is an empty ",(0,l.kt)("inlineCode",{parentName:"p"},"Dict"),", but can be added to either by setting\nit, e.g. ",(0,l.kt)("inlineCode",{parentName:"p"},"self.leixcon_lookup={'Car|noun': ['Z1']}")," or through adding to\nthe existing dictionary, e.g. ",(0,l.kt)("inlineCode",{parentName:"p"},"self.lexicon_lookup['Car|noun'] = ['Z1']"))),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},(0,l.kt)("strong",{parentName:"p"},"lemma","_","lexicon","_","lookup")," : ",(0,l.kt)("inlineCode",{parentName:"p"},"Dict[str, List[str]]")," ",(0,l.kt)("br",null),"\nThe lexicon data structure with only lemma information mapped to a\n",(0,l.kt)("inlineCode",{parentName:"p"},"List")," of USAS semantic tags e.g. ",(0,l.kt)("inlineCode",{parentName:"p"},"{'Car': ['Z2', 'Z1']}"),".\nBy default this is an empty ",(0,l.kt)("inlineCode",{parentName:"p"},"Dict"),", but can be added to either by setting\nit, e.g. ",(0,l.kt)("inlineCode",{parentName:"p"},"self.lemma_leixcon_lookup={'Car': ['Z1']}")," or through adding to\nthe existing dictionary, e.g. ",(0,l.kt)("inlineCode",{parentName:"p"},"self.lemma_lexicon_lookup['Car'] = ['Z1']"))),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},(0,l.kt)("strong",{parentName:"p"},"pos","_","mapper")," : ",(0,l.kt)("inlineCode",{parentName:"p"},"Dict[str, List[str]]"),", optional (default = ",(0,l.kt)("inlineCode",{parentName:"p"},"None"),") ",(0,l.kt)("br",null),"\nIf not ",(0,l.kt)("inlineCode",{parentName:"p"},"None"),", maps from the POS model tagset to the lexicon data POS\ntagset, whereby the mapping is a ",(0,l.kt)("inlineCode",{parentName:"p"},"List")," of tags, the first in the list is\nassumed to be the most relevant and the last to be the least."))),(0,l.kt)("h4",{id:"usasrulebasedtagger.examples"},"Examples",(0,l.kt)("a",{className:"headerlink",href:"#usasrulebasedtagger.examples",title:"Permanent link"},"\xb6")),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"import spacy\nfrom pymusas.spacy_api.taggers import rule_based\n# Construction via spaCy pipeline\nnlp = spacy.blank('en')\n# Using default config\ntagger = nlp.add_pipe('usas_tagger')\ntagger.lemma_lexicon_lookup = {'car': ['Z1']}\ntoken = nlp('car')\nassert token[0]._.usas_tags == ['Z1']\n\n# Construction from class, same defaults as the default config\nfrom pymusas.spacy_api.taggers.rule_based import USASRuleBasedTagger\ntagger = USASRuleBasedTagger()\n\n# Custom config\ncustom_config = {'usas_tags_token_attr': 'semantic_tags'}\nnlp = spacy.blank('en')\ntagger = nlp.add_pipe('usas_tagger', config=custom_config)\ntagger.lemma_lexicon_lookup = {'car': ['Z1']}\ntoken = nlp('car')\nassert token[0]._.semantic_tags == ['Z1']\n")),(0,l.kt)("a",{id:"pymusas.spacy_api.taggers.rule_based.USASRuleBasedTagger.__call__"}),(0,l.kt)("h3",{id:"__call__"},"_","_","call","_","_"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"class USASRuleBasedTagger:\n | ...\n | def __call__(doc: Doc) -> Doc\n")),(0,l.kt)("p",null,"Applies the tagger to the spaCy document, modifies it in place, and\nreturns it. This usually happens under the hood when the ",(0,l.kt)("inlineCode",{parentName:"p"},"nlp")," object is\ncalled on a text and all pipeline components are applied to the ",(0,l.kt)("inlineCode",{parentName:"p"},"Doc")," in\norder."),(0,l.kt)("h4",{id:"__call__.parameters"},"Parameters",(0,l.kt)("a",{className:"headerlink",href:"#__call__.parameters",title:"Permanent link"},"\xb6")),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("strong",{parentName:"li"},"doc")," : ",(0,l.kt)("inlineCode",{parentName:"li"},"Doc")," ",(0,l.kt)("br",null),"\nA ",(0,l.kt)("a",{parentName:"li",href:"https://spacy.io/api/doc"},"spaCy ",(0,l.kt)("inlineCode",{parentName:"a"},"Doc")))),(0,l.kt)("h4",{id:"__call__.returns"},"Returns",(0,l.kt)("a",{className:"headerlink",href:"#__call__.returns",title:"Permanent link"},"\xb6")),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"Doc")," ",(0,l.kt)("br",null))),(0,l.kt)("a",{id:"pymusas.spacy_api.taggers.rule_based.USASRuleBasedTagger.to_bytes"}),(0,l.kt)("h3",{id:"to_bytes"},"to","_","bytes"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"class USASRuleBasedTagger:\n | ...\n | def to_bytes(\n |     self,\n |     *,\n |     exclude: Iterable[str] = SimpleFrozenList()\n | ) -> bytes\n")),(0,l.kt)("p",null,"Serialises the USAS tagger's lexicon lookups and POS mapper to a bytestring."),(0,l.kt)("h4",{id:"to_bytes.parameters"},"Parameters",(0,l.kt)("a",{className:"headerlink",href:"#to_bytes.parameters",title:"Permanent link"},"\xb6")),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("strong",{parentName:"li"},"exclude")," : ",(0,l.kt)("inlineCode",{parentName:"li"},"Iterable[str]"),", optional (default = ",(0,l.kt)("inlineCode",{parentName:"li"},"SimpleFrozenList()"),") ",(0,l.kt)("br",null),"\nThis currently does not do anything, please ignore it.")),(0,l.kt)("h4",{id:"to_bytes.returns"},"Returns",(0,l.kt)("a",{className:"headerlink",href:"#to_bytes.returns",title:"Permanent link"},"\xb6")),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"bytes")," ",(0,l.kt)("br",null))),(0,l.kt)("h4",{id:"to_bytes.examples"},"Examples",(0,l.kt)("a",{className:"headerlink",href:"#to_bytes.examples",title:"Permanent link"},"\xb6")),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"from pymusas.spacy_api.taggers.rule_based import USASRuleBasedTagger\ntagger = USASRuleBasedTagger()\ntagger_bytes = tagger.to_bytes()\n")),(0,l.kt)("a",{id:"pymusas.spacy_api.taggers.rule_based.USASRuleBasedTagger.from_bytes"}),(0,l.kt)("h3",{id:"from_bytes"},"from","_","bytes"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},'class USASRuleBasedTagger:\n | ...\n | def from_bytes(\n |     self,\n |     bytes_data: bytes,\n |     *,\n |     exclude: Iterable[str] = SimpleFrozenList()\n | ) -> "USASRuleBasedTagger"\n')),(0,l.kt)("p",null,"This modifies the USASRuleBasedTagger in place and returns it. It loads\nin the data from the given bytestring."),(0,l.kt)("p",null,"The easiest way to generate a bytestring to load from is through the\n",(0,l.kt)("a",{parentName:"p",href:"#to_bytes"},(0,l.kt)("inlineCode",{parentName:"a"},"to_bytes"))," method."),(0,l.kt)("h4",{id:"from_bytes.parameters"},"Parameters",(0,l.kt)("a",{className:"headerlink",href:"#from_bytes.parameters",title:"Permanent link"},"\xb6")),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},(0,l.kt)("strong",{parentName:"p"},"bytes","_","data")," : ",(0,l.kt)("inlineCode",{parentName:"p"},"bytes")," ",(0,l.kt)("br",null),"\nThe bytestring to load.")),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},(0,l.kt)("strong",{parentName:"p"},"exclude")," : ",(0,l.kt)("inlineCode",{parentName:"p"},"Iterable[str]"),", optional (default = ",(0,l.kt)("inlineCode",{parentName:"p"},"SimpleFrozenList()"),") ",(0,l.kt)("br",null),"\nThis currently does not do anything, please ignore it."))),(0,l.kt)("h4",{id:"from_bytes.returns"},"Returns",(0,l.kt)("a",{className:"headerlink",href:"#from_bytes.returns",title:"Permanent link"},"\xb6")),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("a",{parentName:"li",href:"#usasrulebasedtagger"},(0,l.kt)("inlineCode",{parentName:"a"},"USASRuleBasedTagger"))," ",(0,l.kt)("br",null))),(0,l.kt)("h4",{id:"from_bytes.examples"},"Examples",(0,l.kt)("a",{className:"headerlink",href:"#from_bytes.examples",title:"Permanent link"},"\xb6")),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"from pymusas.spacy_api.taggers.rule_based import USASRuleBasedTagger\ncustom_lexicon = {'example|noun': ['A1']}\ntagger = USASRuleBasedTagger()\ntagger.lexicon_lookup = custom_lexicon\ntagger_bytes = tagger.to_bytes()\nnew_tagger = USASRuleBasedTagger()\n_ = new_tagger.from_bytes(tagger_bytes)\nassert new_tagger.lexicon_lookup == tagger.lexicon_lookup\n")),(0,l.kt)("a",{id:"pymusas.spacy_api.taggers.rule_based.USASRuleBasedTagger.to_disk"}),(0,l.kt)("h3",{id:"to_disk"},"to","_","disk"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"class USASRuleBasedTagger:\n | ...\n | def to_disk(\n |     self,\n |     path: Union[str, Path],\n |     *,\n |     exclude: Iterable[str] = SimpleFrozenList()\n | ) -> None\n")),(0,l.kt)("p",null,"Saves the follwing information, if it exists, to the given ",(0,l.kt)("inlineCode",{parentName:"p"},"path"),", we assume the ",(0,l.kt)("inlineCode",{parentName:"p"},"path"),"\nis an existing directory."),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"lexicon_lookup")," -- as a JSON file at the following path ",(0,l.kt)("inlineCode",{parentName:"li"},"path/lexicon_lookup.json")),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"lemma_lexicon_lookup")," -- as a JSON file at the following path ",(0,l.kt)("inlineCode",{parentName:"li"},"path/lemma_lexicon_lookup.json")),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"pos_mapper")," -- as a JSON file at the following path ",(0,l.kt)("inlineCode",{parentName:"li"},"path/pos_mapper.json"))),(0,l.kt)("h4",{id:"to_disk.parameters"},"Parameters",(0,l.kt)("a",{className:"headerlink",href:"#to_disk.parameters",title:"Permanent link"},"\xb6")),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},(0,l.kt)("strong",{parentName:"p"},"path")," : ",(0,l.kt)("inlineCode",{parentName:"p"},"Union[str, Path]")," ",(0,l.kt)("br",null),"\nPath to an existing direcotry. Path may be either strings or ",(0,l.kt)("inlineCode",{parentName:"p"},"Path"),"-like objects.")),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},(0,l.kt)("strong",{parentName:"p"},"exclude")," : ",(0,l.kt)("inlineCode",{parentName:"p"},"Iterable[str]"),", optional (default = ",(0,l.kt)("inlineCode",{parentName:"p"},"SimpleFrozenList()"),") ",(0,l.kt)("br",null),"\nThis currently does not do anything, please ignore it."))),(0,l.kt)("h4",{id:"to_disk.returns"},"Returns",(0,l.kt)("a",{className:"headerlink",href:"#to_disk.returns",title:"Permanent link"},"\xb6")),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"None")," ",(0,l.kt)("br",null))),(0,l.kt)("h4",{id:"to_disk.examples"},"Examples",(0,l.kt)("a",{className:"headerlink",href:"#to_disk.examples",title:"Permanent link"},"\xb6")),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"from pathlib import Path\nfrom tempfile import TemporaryDirectory\nfrom pymusas.spacy_api.taggers.rule_based import USASRuleBasedTagger\ntagger = USASRuleBasedTagger()\ntagger.lexicon_lookup = {'example|noun': ['A1']}\nwith TemporaryDirectory() as temp_dir:\n    tagger.to_disk(temp_dir)\n    assert Path(temp_dir, 'lexicon_lookup.json').exists()\n    assert not Path(temp_dir, 'lemma_lexicon_lookup.json').exists()\n    assert not Path(temp_dir, 'pos_mapper.json').exists()\n")),(0,l.kt)("a",{id:"pymusas.spacy_api.taggers.rule_based.USASRuleBasedTagger.from_disk"}),(0,l.kt)("h3",{id:"from_disk"},"from","_","disk"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},'class USASRuleBasedTagger:\n | ...\n | def from_disk(\n |     self,\n |     path: Union[str, Path],\n |     *,\n |     exclude: Iterable[str] = SimpleFrozenList()\n | ) -> "USASRuleBasedTagger"\n')),(0,l.kt)("p",null,"Loads the following information in place and returns the USASRuleBasedTagger\nfrom the given ",(0,l.kt)("inlineCode",{parentName:"p"},"path"),", we assume the ",(0,l.kt)("inlineCode",{parentName:"p"},"path")," is an existing directory.\nNone of the following information is required to exist and no error or\ndebug information will be raised or outputted if it does not exist."),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"lexicon_lookup")," -- loads from the following path ",(0,l.kt)("inlineCode",{parentName:"li"},"path/lexicon_lookup.json")),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"lemma_lexicon_lookup")," --  loads from the following path ",(0,l.kt)("inlineCode",{parentName:"li"},"path/lemma_lexicon_lookup.json")),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("inlineCode",{parentName:"li"},"pos_mapper")," -- loads from the following path ",(0,l.kt)("inlineCode",{parentName:"li"},"path/pos_mapper.json"))),(0,l.kt)("h4",{id:"from_disk.parameters"},"Parameters",(0,l.kt)("a",{className:"headerlink",href:"#from_disk.parameters",title:"Permanent link"},"\xb6")),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},(0,l.kt)("strong",{parentName:"p"},"path")," : ",(0,l.kt)("inlineCode",{parentName:"p"},"Union[str, Path]")," ",(0,l.kt)("br",null),"\nPath to an existing direcotry. Path may be either strings or ",(0,l.kt)("inlineCode",{parentName:"p"},"Path"),"-like objects.")),(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("p",{parentName:"li"},(0,l.kt)("strong",{parentName:"p"},"exclude")," : ",(0,l.kt)("inlineCode",{parentName:"p"},"Iterable[str]"),", optional (default = ",(0,l.kt)("inlineCode",{parentName:"p"},"SimpleFrozenList()"),") ",(0,l.kt)("br",null),"\nThis currently does not do anything, please ignore it."))),(0,l.kt)("h4",{id:"from_disk.returns"},"Returns",(0,l.kt)("a",{className:"headerlink",href:"#from_disk.returns",title:"Permanent link"},"\xb6")),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},(0,l.kt)("a",{parentName:"li",href:"#usasrulebasedtagger"},(0,l.kt)("inlineCode",{parentName:"a"},"USASRuleBasedTagger"))," ",(0,l.kt)("br",null))),(0,l.kt)("h4",{id:"from_disk.examples"},"Examples",(0,l.kt)("a",{className:"headerlink",href:"#from_disk.examples",title:"Permanent link"},"\xb6")),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-python"},"from tempfile import TemporaryDirectory\nfrom pymusas.spacy_api.taggers.rule_based import USASRuleBasedTagger\ntagger = USASRuleBasedTagger()\ntagger.lexicon_lookup = {'example|noun': ['A1']}\nnew_tagger = USASRuleBasedTagger()\nwith TemporaryDirectory() as temp_dir:\n    tagger.to_disk(temp_dir)\n    _ = new_tagger.from_disk(temp_dir)\n\nassert new_tagger.lexicon_lookup == tagger.lexicon_lookup\nassert new_tagger.pos_mapper is None\n")))}d.isMDXComponent=!0}}]);