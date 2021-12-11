"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[861],{3905:function(e,t,n){n.d(t,{Zo:function(){return p},kt:function(){return u}});var a=n(7294);function l(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function i(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,a)}return n}function o(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?i(Object(n),!0).forEach((function(t){l(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function r(e,t){if(null==e)return{};var n,a,l=function(e,t){if(null==e)return{};var n,a,l={},i=Object.keys(e);for(a=0;a<i.length;a++)n=i[a],t.indexOf(n)>=0||(l[n]=e[n]);return l}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(a=0;a<i.length;a++)n=i[a],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(l[n]=e[n])}return l}var c=a.createContext({}),s=function(e){var t=a.useContext(c),n=t;return e&&(n="function"==typeof e?e(t):o(o({},t),e)),n},p=function(e){var t=s(e.components);return a.createElement(c.Provider,{value:t},e.children)},m={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},d=a.forwardRef((function(e,t){var n=e.components,l=e.mdxType,i=e.originalType,c=e.parentName,p=r(e,["components","mdxType","originalType","parentName"]),d=s(n),u=l,k=d["".concat(c,".").concat(u)]||d[u]||m[u]||i;return n?a.createElement(k,o(o({ref:t},p),{},{components:n})):a.createElement(k,o({ref:t},p))}));function u(e,t){var n=arguments,l=t&&t.mdxType;if("string"==typeof e||l){var i=n.length,o=new Array(i);o[0]=d;var r={};for(var c in t)hasOwnProperty.call(t,c)&&(r[c]=t[c]);r.originalType=e,r.mdxType="string"==typeof e?e:l,o[1]=r;for(var s=2;s<i;s++)o[s]=n[s];return a.createElement.apply(null,o)}return a.createElement.apply(null,n)}d.displayName="MDXCreateElement"},3190:function(e,t,n){n.r(t),n.d(t,{frontMatter:function(){return r},contentTitle:function(){return c},metadata:function(){return s},toc:function(){return p},default:function(){return d}});var a=n(7462),l=n(3366),i=(n(7294),n(3905)),o=["components"],r={},c=void 0,s={unversionedId:"api/lexicon_collection",id:"api/lexicon_collection",isDocsHomePage:!1,title:"lexicon_collection",description:"pymusas.lexicon_collection",source:"@site/docs/api/lexicon_collection.md",sourceDirName:"api",slug:"/api/lexicon_collection",permalink:"/pymusas/api/lexicon_collection",editUrl:"https://github.com/ucrel/pymusas/edit/main/docs/docs/api/lexicon_collection.md",tags:[],version:"current",lastUpdatedBy:"Paul Rayson",lastUpdatedAt:1639231970,formattedLastUpdatedAt:"12/11/2021",frontMatter:{},sidebar:"api",previous:{title:"file_utils",permalink:"/pymusas/api/file_utils"},next:{title:"pos_mapper",permalink:"/pymusas/api/pos_mapper"}},p=[{value:"LexiconEntry",id:"lexiconentry",children:[{value:"lemma",id:"lemma",children:[],level:4},{value:"semantic_tags",id:"semantic_tags",children:[],level:4},{value:"pos",id:"pos",children:[],level:4}],level:2},{value:"LexiconCollection",id:"lexiconcollection",children:[{value:"add_lexicon_entry",id:"add_lexicon_entry",children:[],level:3},{value:"to_dictionary",id:"to_dictionary",children:[],level:3},{value:"from_tsv",id:"from_tsv",children:[],level:3},{value:"__str__",id:"__str__",children:[],level:3},{value:"__repr__",id:"__repr__",children:[],level:3}],level:2}],m={toc:p};function d(e){var t=e.components,n=(0,l.Z)(e,o);return(0,i.kt)("wrapper",(0,a.Z)({},m,n,{components:t,mdxType:"MDXLayout"}),(0,i.kt)("div",{className:"source-div"},(0,i.kt)("p",null,(0,i.kt)("i",null,"pymusas"),(0,i.kt)("strong",null,".lexicon_collection")),(0,i.kt)("p",null,(0,i.kt)("a",{className:"sourcelink",href:"https://github.com/UCREL/pymusas/blob/main/pymusas/lexicon_collection.py"},"[SOURCE]"))),(0,i.kt)("div",null),(0,i.kt)("hr",null),(0,i.kt)("a",{id:"pymusas.lexicon_collection.LexiconEntry"}),(0,i.kt)("h2",{id:"lexiconentry"},"LexiconEntry"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"@dataclass(init=True, repr=True, eq=True, order=False,\n           unsafe_hash=False, frozen=True)\nclass LexiconEntry\n")),(0,i.kt)("p",null,"A LexiconEntry contains the ",(0,i.kt)("inlineCode",{parentName:"p"},"semantic_tags")," that are associated with a\n",(0,i.kt)("inlineCode",{parentName:"p"},"lemma")," and optionally the lemma's ",(0,i.kt)("inlineCode",{parentName:"p"},"POS"),"."),(0,i.kt)("p",null,"As frozen is true, the attributes cannot be assigned another value."),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Note")," the parameters to the ",(0,i.kt)("inlineCode",{parentName:"p"},"__init__")," are the same as the Instance\nAttributes."),(0,i.kt)("h4",{id:"lexiconentry.instance_attributes"},"Instance Attributes",(0,i.kt)("a",{className:"headerlink",href:"#lexiconentry.instance_attributes",title:"Permanent link"},"\xb6")),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("strong",{parentName:"li"},"lemma")," : ",(0,i.kt)("inlineCode",{parentName:"li"},"str")," ",(0,i.kt)("br",null),"\nThe lemma of a token or the token itself."),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("strong",{parentName:"li"},"semantic","_","tags")," : ",(0,i.kt)("inlineCode",{parentName:"li"},"List[str]")," ",(0,i.kt)("br",null),"\nThe semantic tags associated with the ",(0,i.kt)("inlineCode",{parentName:"li"},"lemma")," and optional ",(0,i.kt)("inlineCode",{parentName:"li"},"POS"),".\nThe semantic tags are in rank order, the most likely tag associated\ntag is the first tag in the list."),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("strong",{parentName:"li"},"pos")," : ",(0,i.kt)("inlineCode",{parentName:"li"},"str"),", optional (default = ",(0,i.kt)("inlineCode",{parentName:"li"},"None"),") ",(0,i.kt)("br",null),"\nThe Part Of Speech (POS) to be associated with the ",(0,i.kt)("inlineCode",{parentName:"li"},"lemma"),".")),(0,i.kt)("a",{id:"pymusas.lexicon_collection.LexiconEntry.lemma"}),(0,i.kt)("h4",{id:"lemma"},"lemma"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"class LexiconEntry:\n | ...\n | lemma: str = None\n")),(0,i.kt)("a",{id:"pymusas.lexicon_collection.LexiconEntry.semantic_tags"}),(0,i.kt)("h4",{id:"semantic_tags"},"semantic","_","tags"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"class LexiconEntry:\n | ...\n | semantic_tags: List[str] = None\n")),(0,i.kt)("a",{id:"pymusas.lexicon_collection.LexiconEntry.pos"}),(0,i.kt)("h4",{id:"pos"},"pos"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"class LexiconEntry:\n | ...\n | pos: Optional[str] = None\n")),(0,i.kt)("a",{id:"pymusas.lexicon_collection.LexiconCollection"}),(0,i.kt)("h2",{id:"lexiconcollection"},"LexiconCollection"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"class LexiconCollection(MutableMapping):\n | ...\n | def __init__(\n |     self,\n |     data: Optional[Dict[str, List[str]]] = None\n | ) -> None\n")),(0,i.kt)("p",null,"This is a dictionary object that will hold ",(0,i.kt)("a",{parentName:"p",href:"#lexiconentry"},(0,i.kt)("inlineCode",{parentName:"a"},"LexiconEntry"))," data in a fast to\naccess object. The keys of the dictionary are expected to be either just a\nlemma or a combination of lemma and pos in the following format:\n",(0,i.kt)("inlineCode",{parentName:"p"},"{lemma}|{pos}")," e.g. ",(0,i.kt)("inlineCode",{parentName:"p"},"Car|Noun"),"."),(0,i.kt)("p",null,"The value to each key is the associated semantic tags, whereby the semantic\ntags are in rank order, the most likely tag is the first tag in the list."),(0,i.kt)("p",null,(0,i.kt)("strong",{parentName:"p"},"Note")," that the ",(0,i.kt)("inlineCode",{parentName:"p"},"lemma")," can be the token\nitself rather than just it's base form, e.g. can be ",(0,i.kt)("inlineCode",{parentName:"p"},"Cars")," rather than ",(0,i.kt)("inlineCode",{parentName:"p"},"Car"),"."),(0,i.kt)("h4",{id:"lexiconcollection.parameters"},"Parameters",(0,i.kt)("a",{className:"headerlink",href:"#lexiconcollection.parameters",title:"Permanent link"},"\xb6")),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("strong",{parentName:"li"},"data")," : ",(0,i.kt)("inlineCode",{parentName:"li"},"Dict[str, List[str]]"),", optional (default = ",(0,i.kt)("inlineCode",{parentName:"li"},"None"),") ",(0,i.kt)("br",null))),(0,i.kt)("h4",{id:"lexiconcollection.instance_attributes"},"Instance Attributes",(0,i.kt)("a",{className:"headerlink",href:"#lexiconcollection.instance_attributes",title:"Permanent link"},"\xb6")),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("strong",{parentName:"li"},"data")," : ",(0,i.kt)("inlineCode",{parentName:"li"},"Dict[str, List[str]]")," ",(0,i.kt)("br",null),"\nDictionary where the keys are ",(0,i.kt)("inlineCode",{parentName:"li"},"{lemma}|{pos}")," and the values are\na list of associated semantic tags. If the ",(0,i.kt)("inlineCode",{parentName:"li"},"data")," parameter given was\n",(0,i.kt)("inlineCode",{parentName:"li"},"None")," then the value of this attribute will be an empty dictionary.")),(0,i.kt)("h4",{id:"lexiconcollection.examples"},"Examples",(0,i.kt)("a",{className:"headerlink",href:"#lexiconcollection.examples",title:"Permanent link"},"\xb6")),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"from pymusas.lexicon_collection import LexiconEntry, LexiconCollection\nlexicon_entry = LexiconEntry('London', ['Z3', 'Z1', 'A1'], 'noun')\ncollection = LexiconCollection()\ncollection.add_lexicon_entry(lexicon_entry)\nmost_likely_tag = collection['London|noun'][0]\nassert most_likely_tag == 'Z3'\nleast_likely_tag = collection['London|noun'][-1]\nassert least_likely_tag == 'A1'\n")),(0,i.kt)("a",{id:"pymusas.lexicon_collection.LexiconCollection.add_lexicon_entry"}),(0,i.kt)("h3",{id:"add_lexicon_entry"},"add","_","lexicon","_","entry"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"class LexiconCollection(MutableMapping):\n | ...\n | def add_lexicon_entry(\n |     self,\n |     value: LexiconEntry,\n |     include_pos: bool = True\n | ) -> None\n")),(0,i.kt)("p",null,"Will add the ",(0,i.kt)("a",{parentName:"p",href:"#lexiconentry"},(0,i.kt)("inlineCode",{parentName:"a"},"LexiconEntry"))," to the collection, whereby the key is the\ncombination of the lemma and pos and the value are the semantic tags."),(0,i.kt)("p",null,"The lemma and pos are combined as follows: ",(0,i.kt)("inlineCode",{parentName:"p"},"{lemma}|{pos}"),", e.g.\n",(0,i.kt)("inlineCode",{parentName:"p"},"Car|Noun")),(0,i.kt)("p",null,"If the pos value is None then then only the lemma is used: ",(0,i.kt)("inlineCode",{parentName:"p"},"{lemma}"),",\ne.g. ",(0,i.kt)("inlineCode",{parentName:"p"},"Car")),(0,i.kt)("h4",{id:"add_lexicon_entry.parameters"},"Parameters",(0,i.kt)("a",{className:"headerlink",href:"#add_lexicon_entry.parameters",title:"Permanent link"},"\xb6")),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("strong",{parentName:"li"},"value")," : ",(0,i.kt)("inlineCode",{parentName:"li"},"LexiconEntry")," ",(0,i.kt)("br",null),"\nLexicon Entry to add to the collection."),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("strong",{parentName:"li"},"include","_","pos")," : ",(0,i.kt)("inlineCode",{parentName:"li"},"bool"),", optional (default = ",(0,i.kt)("inlineCode",{parentName:"li"},"True"),") ",(0,i.kt)("br",null),"\nWhether to include the POS tag within the key.")),(0,i.kt)("a",{id:"pymusas.lexicon_collection.LexiconCollection.to_dictionary"}),(0,i.kt)("h3",{id:"to_dictionary"},"to","_","dictionary"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"class LexiconCollection(MutableMapping):\n | ...\n | def to_dictionary() -> Dict[str, List[str]]\n")),(0,i.kt)("p",null,"Returns the ",(0,i.kt)("inlineCode",{parentName:"p"},"data")," instance attribute."),(0,i.kt)("h4",{id:"to_dictionary.returns"},"Returns",(0,i.kt)("a",{className:"headerlink",href:"#to_dictionary.returns",title:"Permanent link"},"\xb6")),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"Dict[str, List[str]]")," ",(0,i.kt)("br",null))),(0,i.kt)("a",{id:"pymusas.lexicon_collection.LexiconCollection.from_tsv"}),(0,i.kt)("h3",{id:"from_tsv"},"from","_","tsv"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"class LexiconCollection(MutableMapping):\n | ...\n | @staticmethod\n | def from_tsv(\n |     tsv_file_path: Union[PathLike, str],\n |     include_pos: bool = True\n | ) -> Dict[str, List[str]]\n")),(0,i.kt)("p",null,"Given a ",(0,i.kt)("inlineCode",{parentName:"p"},"tsv_file_path")," it will return a dictionary object that can\nbe used to create a ",(0,i.kt)("a",{parentName:"p",href:"#lexiconcollection"},(0,i.kt)("inlineCode",{parentName:"a"},"LexiconCollection")),"."),(0,i.kt)("p",null,"Each line in the TSV file will be read in as a ",(0,i.kt)("a",{parentName:"p",href:"#lexiconentry"},(0,i.kt)("inlineCode",{parentName:"a"},"LexiconEntry")),"\nand added to a temporary ",(0,i.kt)("a",{parentName:"p",href:"#lexiconcollection"},(0,i.kt)("inlineCode",{parentName:"a"},"LexiconCollection")),", once all lines\nin the TSV have been parsed the return value is the ",(0,i.kt)("inlineCode",{parentName:"p"},"data")," attribute of\nthe temporary ",(0,i.kt)("a",{parentName:"p",href:"#lexiconcollection"},(0,i.kt)("inlineCode",{parentName:"a"},"LexiconCollection")),"."),(0,i.kt)("p",null,"If the file path is a URL, the file will be downloaded and cached using\n",(0,i.kt)("a",{parentName:"p",href:"/pymusas/api/file_utils/#download_url_file"},(0,i.kt)("inlineCode",{parentName:"a"},"pymusas.file_utils.download_url_file")),"."),(0,i.kt)("p",null,"If ",(0,i.kt)("inlineCode",{parentName:"p"},"include_pos")," is True and the TSV file does not contain a\n",(0,i.kt)("inlineCode",{parentName:"p"},"pos")," field heading then this will return a LexiconCollection that is\nidentical to a collection that ran this method with ",(0,i.kt)("inlineCode",{parentName:"p"},"include_pos")," equal\nto False."),(0,i.kt)("p",null,"Code reference, the identification of a URL and the idea to do this has\ncome from the ",(0,i.kt)("a",{parentName:"p",href:"https://github.com/allenai/allennlp/blob/main/allennlp/common/file_utils.py#L205"},"AllenNLP library")),(0,i.kt)("h4",{id:"from_tsv.parameters"},"Parameters",(0,i.kt)("a",{className:"headerlink",href:"#from_tsv.parameters",title:"Permanent link"},"\xb6")),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("p",{parentName:"li"},(0,i.kt)("strong",{parentName:"p"},"tsv","_","file","_","path")," : ",(0,i.kt)("inlineCode",{parentName:"p"},"Union[PathLike, str]")," ",(0,i.kt)("br",null),"\nA file path or URL to a TSV file that contains at least two\nfields, with an optional third, with the following headings:"),(0,i.kt)("ol",{parentName:"li"},(0,i.kt)("li",{parentName:"ol"},(0,i.kt)("p",{parentName:"li"},(0,i.kt)("inlineCode",{parentName:"p"},"lemma"),",")),(0,i.kt)("li",{parentName:"ol"},(0,i.kt)("p",{parentName:"li"},(0,i.kt)("inlineCode",{parentName:"p"},"semantic_tags"))),(0,i.kt)("li",{parentName:"ol"},(0,i.kt)("p",{parentName:"li"},(0,i.kt)("inlineCode",{parentName:"p"},"pos")," (Optional)"),(0,i.kt)("p",{parentName:"li"},"All other fields will be ignored.")))),(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("p",{parentName:"li"},(0,i.kt)("strong",{parentName:"p"},"include","_","pos")," : ",(0,i.kt)("inlineCode",{parentName:"p"},"bool"),", optional (default = ",(0,i.kt)("inlineCode",{parentName:"p"},"True"),") ",(0,i.kt)("br",null),"\nWhether to include the POS information, if the information is avaliable,\nor not. See ",(0,i.kt)("a",{parentName:"p",href:"#add_lexicon_entry"},(0,i.kt)("inlineCode",{parentName:"a"},"add_lexicon_entry"))," for more information on this\nparameter."))),(0,i.kt)("h4",{id:"from_tsv.returns"},"Returns",(0,i.kt)("a",{className:"headerlink",href:"#from_tsv.returns",title:"Permanent link"},"\xb6")),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"Dict[str, List[str]]")," ",(0,i.kt)("br",null))),(0,i.kt)("h4",{id:"from_tsv.raises"},"Raises",(0,i.kt)("a",{className:"headerlink",href:"#from_tsv.raises",title:"Permanent link"},"\xb6")),(0,i.kt)("ul",null,(0,i.kt)("li",{parentName:"ul"},(0,i.kt)("inlineCode",{parentName:"li"},"ValueError")," ",(0,i.kt)("br",null),"\nIf the minimum field headings, ",(0,i.kt)("inlineCode",{parentName:"li"},"lemma")," and ",(0,i.kt)("inlineCode",{parentName:"li"},"semantic_tags"),", do not\nexist in the given TSV file.")),(0,i.kt)("h4",{id:"from_tsv.examples"},"Examples",(0,i.kt)("a",{className:"headerlink",href:"#from_tsv.examples",title:"Permanent link"},"\xb6")),(0,i.kt)("p",null,(0,i.kt)("inlineCode",{parentName:"p"},"include_pos")," = ",(0,i.kt)("inlineCode",{parentName:"p"},"True")),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"from pymusas.lexicon_collection import LexiconCollection\nwelsh_lexicon_url = 'https://raw.githubusercontent.com/apmoore1/Multilingual-USAS/master/Welsh/semantic_lexicon_cy.tsv'\nwelsh_lexicon_dict = LexiconCollection.from_tsv(welsh_lexicon_url, include_pos=True)\nwelsh_lexicon_collection = LexiconCollection(welsh_lexicon_dict)\nassert welsh_lexicon_dict['ceir|noun'][0] == 'M3fn'\nassert welsh_lexicon_dict['ceir|verb'][0] == 'A9+'\n")),(0,i.kt)("p",null,(0,i.kt)("inlineCode",{parentName:"p"},"include_pos")," = ",(0,i.kt)("inlineCode",{parentName:"p"},"False")),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"from pymusas.lexicon_collection import LexiconCollection\nwelsh_lexicon_url = 'https://raw.githubusercontent.com/apmoore1/Multilingual-USAS/master/Welsh/semantic_lexicon_cy.tsv'\nwelsh_lexicon_dict = LexiconCollection.from_tsv(welsh_lexicon_url, include_pos=False)\nwelsh_lexicon_collection = LexiconCollection(welsh_lexicon_dict)\nassert welsh_lexicon_dict['ceir'][0] == 'M3fn'\n")),(0,i.kt)("a",{id:"pymusas.lexicon_collection.LexiconCollection.__str__"}),(0,i.kt)("h3",{id:"__str__"},"_","_","str","_","_"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"class LexiconCollection(MutableMapping):\n | ...\n | def __str__() -> str\n")),(0,i.kt)("p",null,"Human readable string."),(0,i.kt)("a",{id:"pymusas.lexicon_collection.LexiconCollection.__repr__"}),(0,i.kt)("h3",{id:"__repr__"},"_","_","repr","_","_"),(0,i.kt)("pre",null,(0,i.kt)("code",{parentName:"pre",className:"language-python"},"class LexiconCollection(MutableMapping):\n | ...\n | def __repr__() -> str\n")),(0,i.kt)("p",null,"Machine readable string. When printed and run ",(0,i.kt)("inlineCode",{parentName:"p"},"eval()")," over the string\nyou should be able to recreate the object."))}d.isMDXComponent=!0}}]);