"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[985],{3905:function(e,t,a){a.d(t,{Zo:function(){return u},kt:function(){return g}});var n=a(7294);function o(e,t,a){return t in e?Object.defineProperty(e,t,{value:a,enumerable:!0,configurable:!0,writable:!0}):e[t]=a,e}function r(e,t){var a=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),a.push.apply(a,n)}return a}function i(e){for(var t=1;t<arguments.length;t++){var a=null!=arguments[t]?arguments[t]:{};t%2?r(Object(a),!0).forEach((function(t){o(e,t,a[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(a)):r(Object(a)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(a,t))}))}return e}function s(e,t){if(null==e)return{};var a,n,o=function(e,t){if(null==e)return{};var a,n,o={},r=Object.keys(e);for(n=0;n<r.length;n++)a=r[n],t.indexOf(a)>=0||(o[a]=e[a]);return o}(e,t);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);for(n=0;n<r.length;n++)a=r[n],t.indexOf(a)>=0||Object.prototype.propertyIsEnumerable.call(e,a)&&(o[a]=e[a])}return o}var l=n.createContext({}),p=function(e){var t=n.useContext(l),a=t;return e&&(a="function"==typeof e?e(t):i(i({},t),e)),a},u=function(e){var t=p(e.components);return n.createElement(l.Provider,{value:t},e.children)},c={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},d=n.forwardRef((function(e,t){var a=e.components,o=e.mdxType,r=e.originalType,l=e.parentName,u=s(e,["components","mdxType","originalType","parentName"]),d=p(a),g=o,m=d["".concat(l,".").concat(g)]||d[g]||c[g]||r;return a?n.createElement(m,i(i({ref:t},u),{},{components:a})):n.createElement(m,i({ref:t},u))}));function g(e,t){var a=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var r=a.length,i=new Array(r);i[0]=d;var s={};for(var l in t)hasOwnProperty.call(t,l)&&(s[l]=t[l]);s.originalType=e,s.mdxType="string"==typeof e?e:o,i[1]=s;for(var p=2;p<r;p++)i[p]=a[p];return n.createElement.apply(null,i)}return n.createElement.apply(null,a)}d.displayName="MDXCreateElement"},6864:function(e,t,a){a.r(t),a.d(t,{frontMatter:function(){return s},contentTitle:function(){return l},metadata:function(){return p},toc:function(){return u},default:function(){return d}});var n=a(3117),o=a(102),r=(a(7294),a(3905)),i=["components"],s={slug:"/using",title:"Using PyMUSAS",sidebar_position:3},l="Using PyMUSAS",p={unversionedId:"usage/getting_started/using_pymusas",id:"usage/getting_started/using_pymusas",title:"Using PyMUSAS",description:"PyMUSAS, currently, is most effective when used with one of the spaCy models and a Ucrel Semantic Analysis System (USAS) single word lexicon, of which the Multilingual USAS repository contains USAS lexicons for 14 languages.",source:"@site/docs/usage/getting_started/using_pymusas.md",sourceDirName:"usage/getting_started",slug:"/using",permalink:"/pymusas/using",editUrl:"https://github.com/ucrel/pymusas/edit/main/docs/docs/usage/getting_started/using_pymusas.md",tags:[],version:"current",lastUpdatedBy:"Andrew Moore",lastUpdatedAt:1642503331,formattedLastUpdatedAt:"1/18/2022",sidebarPosition:3,frontMatter:{slug:"/using",title:"Using PyMUSAS",sidebar_position:3},sidebar:"docs",previous:{title:"Installation",permalink:"/pymusas/installation"},next:{title:"Tag Text",permalink:"/pymusas/usage/how_to/tag_text"}},u=[{value:"Background information on the tagger",id:"background-information-on-the-tagger",children:[],level:2},{value:"Adding the tagger to an existing spaCy pipeline",id:"adding-the-tagger-to-an-existing-spacy-pipeline",children:[],level:2},{value:"Applying it to some text",id:"applying-it-to-some-text",children:[],level:2},{value:"Saving the tagger",id:"saving-the-tagger",children:[],level:2}],c={toc:u};function d(e){var t=e.components,a=(0,o.Z)(e,i);return(0,r.kt)("wrapper",(0,n.Z)({},c,a,{components:t,mdxType:"MDXLayout"}),(0,r.kt)("h1",{id:"using-pymusas"},"Using PyMUSAS"),(0,r.kt)("p",null,"PyMUSAS, currently, is most effective when used with one of the ",(0,r.kt)("a",{parentName:"p",href:"https://spacy.io/models"},"spaCy models")," and a Ucrel Semantic Analysis System (USAS) single word lexicon, of which the ",(0,r.kt)("a",{parentName:"p",href:"https://github.com/UCREL/Multilingual-USAS"},"Multilingual USAS repository")," contains USAS lexicons for 14 languages. "),(0,r.kt)("p",null,"In this guide we are going to go over the main features of the ",(0,r.kt)("a",{parentName:"p",href:"/api/spacy_api/taggers/rule_based"},"USASRuleBasedTagger"),", from now on called the USAS tagger, which are:"),(0,r.kt)("ol",null,(0,r.kt)("li",{parentName:"ol"},"Background information on the tagger"),(0,r.kt)("li",{parentName:"ol"},"Adding the tagger to an existing spaCy pipeline"),(0,r.kt)("li",{parentName:"ol"},"Applying it to some text"),(0,r.kt)("li",{parentName:"ol"},"Saving the tagger. ")),(0,r.kt)("p",null,"The example use case will be tagging the the first sentence of a Portuguese Wikipedia article on the ",(0,r.kt)("a",{parentName:"p",href:"https://pt.wikipedia.org/wiki/Parque_Nacional_da_Peneda-Ger%C3%AAs"},"Peneda-Ger\xeas national park")," (",(0,r.kt)("a",{parentName:"p",href:"https://en.wikipedia.org/wiki/Peneda-Ger%C3%AAs_National_Park"},"English link")," to the Wikipedia article)."),(0,r.kt)("h2",{id:"background-information-on-the-tagger"},"Background information on the tagger"),(0,r.kt)("p",null,"The UCREL tagger is a rule based token level semantic tagger, it has been specifically developed for the ",(0,r.kt)("a",{parentName:"p",href:"https://ucrel.lancs.ac.uk/usas/"},"USAS tagset"),", but has been created so that it can be used with any other semantic tagset. For more information on the UCREL tagger see the ",(0,r.kt)("a",{parentName:"p",href:"/api/spacy_api/taggers/rule_based#usasrulebasedtagger"},"USASRuleBasedTagger class docstring in the API pages")," which includes the list of rules the tagger applies. The rest of this guide can be read without any of this background knowledge."),(0,r.kt)("h2",{id:"adding-the-tagger-to-an-existing-spacy-pipeline"},"Adding the tagger to an existing spaCy pipeline"),(0,r.kt)("p",null,"As the Wikipedia article is in Portuguese we will need to download the Portuguese spaCy pipeline, in this case we downloaded the small version, but any version can be used:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-bash"},"python -m spacy download pt_core_news_sm\n")),(0,r.kt)("p",null,"To add the ",(0,r.kt)("a",{parentName:"p",href:"/api/spacy_api/taggers/rule_based"},"USAS tagger")," to this existing pipeline:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"import spacy\nfrom pymusas.spacy_api.taggers import rule_based\n# We exclude ['parser', 'ner'] as these components are typically not needed\n# for the USAS tagger\nnlp = spacy.load('pt_core_news_sm', exclude=['parser', 'ner'])\n# Adds the tagger to the pipeline and returns the tagger \nusas_tagger = nlp.add_pipe('usas_tagger')\n_ = nlp.analyze_pipes(pretty=True)\n")),(0,r.kt)("p",null,"The output from ",(0,r.kt)("inlineCode",{parentName:"p"},"nlp.analyze_pipes(pretty=True)")," is shown below:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-bash"},"============================= Pipeline Overview =============================\n\n#   Component         Assigns             Requires      Scores           Retokenizes\n-   ---------------   -----------------   -----------   --------------   -----------\n0   tok2vec           doc.tensor                                         False      \n                                                                                    \n1   morphologizer     token.morph                       pos_acc          False      \n                      token.pos                         morph_acc                   \n                                                        morph_per_feat              \n                                                                                    \n2   attribute_ruler                                                      False      \n                                                                                    \n3   lemmatizer        token.lemma                       lemma_acc        False      \n                                                                                    \n4   usas_tagger       token._.usas_tags   token.lemma                    False      \n                                          token.pos                                 \n\n\u2714 No problems found.\n")),(0,r.kt)("p",null,"As we can see the ",(0,r.kt)("a",{parentName:"p",href:"/api/spacy_api/taggers/rule_based"},"USAS tagger")," has been added and is called ",(0,r.kt)("inlineCode",{parentName:"p"},"usas_tagger"),". We can see from this pipeline overview that the tagger requires both the ",(0,r.kt)("inlineCode",{parentName:"p"},"token.lemma"),", which comes from the ",(0,r.kt)("inlineCode",{parentName:"p"},"lemmatizer"),", and the ",(0,r.kt)("inlineCode",{parentName:"p"},"token.pos"),", which comes from the ",(0,r.kt)("inlineCode",{parentName:"p"},"morphologizer"),", attributes. In general the USAS tagger is more effective when it has access to Part Of Speech (POS) and the lemma of each token. However the USAS tagger can be used without either of these components, but it might make the tagger less accurate."),(0,r.kt)("h2",{id:"applying-it-to-some-text"},"Applying it to some text"),(0,r.kt)("p",null,"Before using the added tagger we need to add the single word Portuguese USAS lexicon to the tagger, to do this we first need to download the lexicon form the ",(0,r.kt)("a",{parentName:"p",href:"https://github.com/UCREL/Multilingual-USAS"},"Multilingual USAS repository")," and then add the lexicon with and without the POS information (the code example below carries on from the previous)."),(0,r.kt)("div",{className:"admonition admonition-note alert alert--secondary"},(0,r.kt)("div",{parentName:"div",className:"admonition-heading"},(0,r.kt)("h5",{parentName:"div"},(0,r.kt)("span",{parentName:"h5",className:"admonition-icon"},(0,r.kt)("svg",{parentName:"span",xmlns:"http://www.w3.org/2000/svg",width:"14",height:"16",viewBox:"0 0 14 16"},(0,r.kt)("path",{parentName:"svg",fillRule:"evenodd",d:"M6.3 5.69a.942.942 0 0 1-.28-.7c0-.28.09-.52.28-.7.19-.18.42-.28.7-.28.28 0 .52.09.7.28.18.19.28.42.28.7 0 .28-.09.52-.28.7a1 1 0 0 1-.7.3c-.28 0-.52-.11-.7-.3zM8 7.99c-.02-.25-.11-.48-.31-.69-.2-.19-.42-.3-.69-.31H6c-.27.02-.48.13-.69.31-.2.2-.3.44-.31.69h1v3c.02.27.11.5.31.69.2.2.42.31.69.31h1c.27 0 .48-.11.69-.31.2-.19.3-.42.31-.69H8V7.98v.01zM7 2.3c-3.14 0-5.7 2.54-5.7 5.68 0 3.14 2.56 5.7 5.7 5.7s5.7-2.55 5.7-5.7c0-3.15-2.56-5.69-5.7-5.69v.01zM7 .98c3.86 0 7 3.14 7 7s-3.14 7-7 7-7-3.12-7-7 3.14-7 7-7z"}))),"note")),(0,r.kt)("div",{parentName:"div",className:"admonition-content"},(0,r.kt)("p",{parentName:"div"},"When it downloads the lexicon it will be saved within the ",(0,r.kt)("a",{parentName:"p",href:"/api/config"},"PYMUSAS_CACHE_HOME")," directory for caching, which by default is set to ",(0,r.kt)("inlineCode",{parentName:"p"},"~/.cache/pymusas"),", this can be changed either by setting ",(0,r.kt)("inlineCode",{parentName:"p"},"pymusas.config.PYMUSAS_CACHE_HOME")," within the code you are writing or by setting the ",(0,r.kt)("inlineCode",{parentName:"p"},"PYMUSAS_HOME")," environment variable."))),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"from pymusas.file_utils import download_url_file\nfrom pymusas.lexicon_collection import LexiconCollection\n\nportuguese_usas_lexicon_url = 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Portuguese/semantic_lexicon_pt.tsv'\nportuguese_usas_lexicon_file = download_url_file(portuguese_usas_lexicon_url)\n# Includes the POS information\nportuguese_lexicon_lookup = LexiconCollection.from_tsv(portuguese_usas_lexicon_file)\n# excludes the POS information\nportuguese_lemma_lexicon_lookup = LexiconCollection.from_tsv(portuguese_usas_lexicon_file, \n                                                             include_pos=False)\n# Add the lexicon information to the USAS tagger within the pipeline\nusas_tagger.lexicon_lookup = portuguese_lexicon_lookup\nusas_tagger.lemma_lexicon_lookup = portuguese_lemma_lexicon_lookup\n")),(0,r.kt)("p",null,"In addition we need to add a POS mapper for the ",(0,r.kt)("a",{parentName:"p",href:"/api/spacy_api/taggers/rule_based"},"USAS tagger"),", as currently all of the USAS lexicons use the USAS core tagset whereas the spaCy POS models uses the UPOS tagset, therefore we need to add a mapping dictionary, ",(0,r.kt)("a",{parentName:"p",href:"/api/pos_mapper"},"UPOS_TO_USAS_CORE"),", which will convert the POS tags outputted from the POS model from the UPOS tagset to the USAS core tagset. This is done by adding the following:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"from pymusas.pos_mapper import UPOS_TO_USAS_CORE\n\nusas_tagger.pos_mapper = UPOS_TO_USAS_CORE\n")),(0,r.kt)("p",null,"We can now apply the tagger to the first sentence from the ",(0,r.kt)("a",{parentName:"p",href:"https://pt.wikipedia.org/wiki/Parque_Nacional_da_Peneda-Ger%C3%AAs"},"Peneda-Ger\xeas national park")," Wikipedia article using the standard spaCy syntax:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},'text = "O Parque Nacional da Peneda-Ger\xeas \xe9 uma \xe1rea protegida de Portugal, com autonomia administrativa, financeira e capacidade jur\xeddica, criada no ano de 1971, no meio ambiente da Peneda-Ger\xeas."\n\noutput_doc = nlp(text)\n')),(0,r.kt)("p",null,"We can then output the token, lemma, POS, and USAS tags for each token as follows:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"print(f'Text\\tLemma\\tPOS\\tUSAS Tags')\nfor token in output_doc:\n    print(f'{token.text}\\t{token.lemma_}\\t{token.pos_}\\t{token._.usas_tags}')\n")),(0,r.kt)("p",null,"Output:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-tsv"},"Text    Lemma   POS     USAS Tags\nO       O       DET     ['Z5']\nParque  Parque  PROPN   ['M2']\nNacional        Nacional        PROPN   ['M7/S2mf']\nda      da      ADP     ['Z5']\nPeneda-Ger\xeas    Peneda-Ger\xeas    PROPN   ['Z99']\n\xe9       ser     AUX     ['A3+', 'Z5']\numa     umar    DET     ['Z99']\n\xe1rea    \xe1rea    NOUN    ['H2/S5+c', 'X2.2', 'M7', 'A4.1', 'N3.6']\nprotegida       protegido       ADJ     ['O4.5/A2.1', 'S1.2.5+']\nde      de      ADP     ['Z5']\nPortugal        Portugal        PROPN   ['Z2', 'Z3c']\n,       ,       PUNCT   ['PUNCT']\ncom     com     ADP     ['Z5']\nautonomia       autonomia       NOUN    ['A1.7-', 'G1.1/S7.1+', 'X6+/S5-', 'S5-']\nadministrativa  administrativo  ADJ     ['S7.1+']\n,       ,       PUNCT   ['PUNCT']\nfinanceira      financeiro      ADJ     ['I1', 'I1/G1.1']\ne       e       CCONJ   ['Z5']\ncapacidade      capacidade      NOUN    ['N3.2', 'N3.4', 'N5.1+', 'X9.1+', 'I3.1', 'X9.1']\njur\xeddica        jur\xeddico        ADJ     ['G2.1']\n,       ,       PUNCT   ['PUNCT']\ncriada  criar   VERB    ['I3.1/B4/S2.1f', 'S2.1f%', 'S7.1-/S2mf']\nno      o       ADP     ['Z5']\nano     ano     NOUN    ['T1.3', 'P1c']\nde      de      ADP     ['Z5']\n1971    1971    NUM     ['N1']\n,       ,       PUNCT   ['PUNCT']\nno      o       ADP     ['Z5']\nmeio    mear    ADJ     ['M6', 'N5', 'N4', 'T1.2', 'N2', 'X4.2', 'I1.1', 'M3/H3', 'N3.3', 'A4.1', 'A1.1.1', 'T1.3']\nambiente        ambientar       NOUN    ['W5', 'W3', 'E1', 'Y2', 'O4.1']\nda      da      ADP     ['Z5']\nPeneda-Ger\xeas    Peneda-Ger\xeas    PROPN   ['Z99']\n.       .       PUNCT   ['PUNCT']\n")),(0,r.kt)("p",null,"We can see above the USAS tags are outputted as a ",(0,r.kt)("inlineCode",{parentName:"p"},"List"),", of which the first tag in the ",(0,r.kt)("inlineCode",{parentName:"p"},"List")," is always the most likely tag."),(0,r.kt)("h2",{id:"saving-the-tagger"},"Saving the tagger"),(0,r.kt)("p",null,"To save yourself from having to add the lexicon to the tagger, and then add the POS mapper you may wish to instead save this spaCy pipeline as it is currently to then load back up. To save the pipeline to disk you can use the standard spaCy method of ",(0,r.kt)("inlineCode",{parentName:"p"},"to_disk")," as follows:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"nlp.to_disk('PATH TO DIRECTORY')\n")),(0,r.kt)("p",null,"And then to load the pipeline back up"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},"import spacy\n\nnlp = spacy.load('PATH TO DIRECTORY')\n")))}d.isMDXComponent=!0}}]);