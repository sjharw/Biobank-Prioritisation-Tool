# Project Background

## About the project
Biobanks have been established to safeguard existing genetic diversity by freezing biological animal material that can be used in research or later
be defrosted and used to reintroduce genetic diversity into ex-situ and in-situ populations. Unfortunately, biobanks face challenges such as high operational costs and limited funding, and they must prioritise their efforts. This tool has been developed to assist biobanks with prioritising species for sample collection so they can optimise their resource usage and allocation.

This tool takes into account the species **conservation value** (IUCN Category, CITES Appendix, and EDGE Score), 
the **demand** (requests) for samples from that species, 
and the number of **samples** already present within the biobank. 
Species with high conservation value will have higher priority scores because they have greater risk of extinction and greater evolutionary distinctiveness.
The same goes for species with higher demand for samples.
Species with fewer samples in biobanks receive higher scores than those with greater numbers of samples in storage, as a lack of samples pose greater risk of losing that species genetic information.
These category scores are used to calculate a priority score for each species which can be used to rank the species.

The projects adopts an alterated version of the [MAPISCo methodology](https://github.com/DrMattG/MAPISCo) to generate the priority scores.
The method involves converting any string data to a numeric form, normalising the individual dataset scores by diving/ inverting by the maximum, combining the datasets into their corresponding category by taking their mean, applying a weight to this category, and then taking the mean of the weighted categories to produce a priority score that ranks species.

The tool is currently problematic with handling missing data, 
it assigns values of zero to missing data which artificially reduces the overall priority scores, 
thus penalising species that have missing data. 
This issue is due to be addressed in later versions of the tool.

## About the developer
[Sarah](https://www.linkedin.com/in/sarah-j-harwood) is a Data Engineer with a background in genetics and conservation biology. She was introduced into the world of biobanking when she met [Mike Bruford](https://www.cardiff.ac.uk/people/view/81128-bruford-mike) who offered her a placement year with [The Frozen Ark](https://www.frozenark.org/). During this time, Sarah upskilled in Data Engineering in R & SQL. Since her placement year she has worked with various technologies, including Python, PySpark, Neo4j, ArangoDB, and Azure. Using her newfound skills, Sarah has volunteered with CryoArks to re-develop the Prioritisation Tool as a Python Flask application to practice Python Software Development and produce a useful tool that can be used by biobanks. This is her first full-stack application and it is in ongoing development.

## About the datasources

### CryoArks
[CryoArks biobank](https://www.cryoarks.org/) is an initiative that aims to bring together the diverse collections of animal frozen material found in museums, zoos, research institutes and universities across the UK to make them accessible to the UK’s research and conservation community. The CryoArks dataset provides counts of the number of samples stored for each species across the CryoArks collection. The dataset provided in this app has been cleaned and processed, it is not the original CryoArks dataset.

### CITES
[Convention on International Trade in Endangered Species of Wild Fauna and Flora](https://cites.org/eng/disc/species.php) (CITES) is a multilateral treaty to protect endangered plants and animals from the threats of international trade. CITES operates through a system of permits and certificates that control the import, export, and re-export of protected species. It categorizes species into three appendices based on their conservation status and the level of protection required. Appendix I includes the most endangered species, for which commercial trade is generally prohibited. Appendix II covers species that are not necessarily threatened with extinction but that may become so unless trade is closely controlled. Appendix III lists species protected by at least one member country that requests cooperation from other countries to control their trade. 

CITES provide access to the Species+ database through the [Species+/CITES Checklist API](https://api.speciesplus.net/). Each row of data in the Species+ database represents a single taxon concept (a distinct species) and their corrosponding CITES Appendix. The taxon concept is defined by a unique combination of a scientific name and its corresponding author/year.

### IUCN
The [International Union for Conservation of Nature](https://www.iucn.org/) (IUCN) is a globally recognized organization dedicated to promoting sustainable development and the conservation of biodiversity. IUCN maintains the [Red List of Threatened Species](https://www.iucnredlist.org/), a comprehensive database that assesses the conservation status of thousands of species worldwide. The IUCN Red List is a critical indicator of the health of the world’s biodiversity. It provides information about range, population size, habitat and ecology, use and/or trade, threats, and conservation actions that will help inform necessary conservation decisions. IUCN provides access to the Red List database through the [IUCN Red List API](http://apiv3.iucnredlist.org/).

### EDGE
[The Evolutionarily Distinct and Globally Endangered](https://www.edgeofexistence.org/species/) (EDGE) organization is a conservation initiative that focuses on identifying and protecting the world's most unique and endangered species. Established by the Zoological Society of London (ZSL), EDGE aims to prioritize species that have few close relatives and are at high risk of extinction. These species often represent distinct branches of the evolutionary tree and have unique adaptations and ecological roles. EDGE provide access to their EDGE lists thought the [EDGE List site](https://www.edgeofexistence.org/edge-lists/).
