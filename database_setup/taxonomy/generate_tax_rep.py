####------------------------- Creating dictionaries of taxonomy replacement values ---------------------------####
###--- Library imports
import json
from configparser import ConfigParser

# Set up paths
config = ConfigParser()
config.read("config.ini")
TAXON = config["PATHS"]["taxa_dir"]

##---------------- Class --------------##
class_tax = {
    "Actinopteri": "Actinopterygii",
    "Enopla": "Hoplonemertea",  # Missclassification in Nemertina
    "Hirudinoidea": "Clitellata",  # Missclassification (Hirudinoidea is subclass)
}

multi_class = {
    **dict.fromkeys(["Onychophora", "Turbellaria"], "Not assigned"),
    **dict.fromkeys(
        ["Coelacanthi", "Dipneusti"], "Sarcopterygii"
    ),  # Missclassification
}


all_class = {"class": {**class_tax, **multi_class}}


##---------------- Family --------------##
family = {
    "Columbidnae": "Columbidae",  # spelling/grammar error in Aves
    "Helostomatidae": "Helostomatidae",  # spelling/grammar error in Actinopterygii
    "Istophoridae": "Istiophoridae",  # spelling/grammar error in Actinopterygii
    "Tettigonioidea": "Tettigoniidae",  # spelling/grammar error in Arthropoda
    "Heterocephalidae": "Bathyergidae",  # Missclassification in Mammalia
    "Tridacnidae": "Cardiidae",  # Missclassification in Mollusca
    "Grimpoteuthididae": "Opisthoteuthidae",  # Missclassification in mollusca
    "Macromiidae": "Corduliidae",  # Missclassification (Macromiidae is subfamilyin insecta
    "Centracanthidae": "Sparidae",  # Missclassification in Actinopterygii
    "Oleacinidae": "Spiraxidae",  # Missclassificaiton in mollusca
    "Calamariidae": "Colubridae",  # Missclassification (Calamariidae is subfamily)
    "Aphaniidae": "Cyprinodontidae",  # Missclassification in Actinopterygii
    "Sundasalangidae": "Clupeidae",  # Missclassification in Actinopterygii
    "Xiphocarididae": "Atyidae",  # Missclassification (Xiphocarididae considered as family Atyidaein Crustacea
    "Blattellidae": "Ectobiidae",  # Missclassification (Ectobiidae formally was Blattellidae)
    "Dinematichthyidae": "Bythitidae",  # Missclassification in Actinopterygii
    "Callaeidae": "Callaeatidae",  # spelling/grammar error
    "Pityriasidae": "Pityriaseidae",  # spelling/grammar error
    "Platylophidae": "Corvidae",  # Missclassification in aves
    "Cicindelidae": "Carabidae",  # Missclassification (Cicindelinae  is subfamily)
    "Hypolestidae": "Megapodagrionidae",  # Missclassification (Hypolestidae is subfamilyin insecta
    "Batillaridae": "Batillariidae",  # spelling/grammar error
    "Trachyphylliidae": "Merulinidae",  # Missclassification corals
    "Lottidae": "Lottiidae",  # spelling/grammar error
    "Subulinidae": "Achatinidae",  # Missclassification (Subulinidae is a subfamily)
    "Polyphagidae": "Corydiidae",  # Synonym
    "Carciniphoridae": "Anisolabididae",  # Synonym
    "Phrynoidea": "Phrynichidae",  # spelling/grammar error
    "Charinoidea": "Charinidae",  # spelling/grammar error
    "Zoriidae": "Miturgidae",
    "Xenophiidae": "Xenophidiidae",  # spelling/grammar error
    "Telmatobiidae": "Ceratophryidae",  # Missclassification (Telmatobiidae is subfamily)
    "Oceanitidae": "Hydrobatidae",  #
    "Pneumoroidae": "Pneumoridae",  # spelling/grammar error
    "Spiroboleliidae": "Spirobolellidae",  # spelling/grammar error
    "Nephilidae": "Araneidae",  # Missclassification (Nephilidae is subfamilyin arachnida
    "Prodidomidae": "Gnaphosidae",  # Missclassification in arachnida
    "Ascaphidae": "Leiopelmatidae",  # Missclassification in anura
    "Chlamyphoridae": "Dasypodidae",  # Missclassification mammalia
    "Prionodontidae": "Viverridae",  # Missclassification
    "Conrauidae": "Petropedetidae",  # Missclassification (Conraua included so Conrauidae family not formed)
    "Allophrynidae": "Centrolenidae",
    "Phyllomedusidae": "Hylidae",
    "Chlorogomphidae": "Cordulegastridae",  # Missclasisfication
    "Philogangidae": "Lestoideidae",  # Missclassification
    "Pectiniidae": "Lobophylliidae",  # Revision of families
    "Ziphiidae": "Hyperoodontidae",  # Synonym
    "Labiidae": "Spongiphoridae",  # Synonym
    "Helostomatidae": "Helostomatidae",  # spelling/grammar error
    "Pteroclidae": "Pteroclididae",  # spelling/grammar error
    "Leiotrichidae": "Leiothrichidae",  # spelling/grammar error
    "Passerellidae": "Emberizidae",  # Missclassification aves
    "Modulatricidae": "Arcanatoridae",  # Missclassification aves
    "Prosymnidae": "Lamprophiidae",  # spelling and missclassification
    "Bolyeriidae": "Bolyeridae",  # spelling/grammar error
    "Meandriniidae": "Meandrinidae",  # spelling/grammar error
    "Rhinopteridae": "Myliobatidae",  # Missclassification(Rhinopteridae is subfamily)
}

multi_family = {
    **dict.fromkeys(
        ["Megalaimidae", "Lybiidae"], "Ramphastidae"
    ),  # Missclassification in Aves
    **dict.fromkeys(
        ["Psittaculidae", "Cacatuidae", "Loriidae"], "Psittacidae"
    ),  # Spelling/grammar and missclassisifation in Aves
    **dict.fromkeys(
        ["Typhlonectidae", "Dermophiidae"], "Caeciliidae"
    ),  # Missclassification in Amphibia
    **dict.fromkeys(
        [
            "Philosinidae",
            "Thaumatoneuridae",
            "Philogeniidae",
            "Heteragrionidae",
            "Argiolestidae",
        ],
        "Megapodagrionidae",
    ),  # Missclassification (these ae subfamilies)
    **dict.fromkeys(
        ["Pentaphlebiidae", "Rimanellidae", "Devadattidae"], "Amphipterygidae"
    ),  # missclassification arthropoda
    **dict.fromkeys(
        [
            "Liochelidae",
            "Hadogeninae",
            "Opisthacanthinae",
            "Ischnuridae",
            "Protoischnuridae",
        ],
        "Hormuridae",
    ),  # Missclassification in arachnida
    **dict.fromkeys(
        ["Calyptophilidae", "Rhodinocichlidae", "Phaenicophilidae"], "Thraupidae"
    ),  # Missclassification in aves
    **dict.fromkeys(
        ["Psammophiidae", "Atractaspididae", "Pseudoxyrhophiidae"], "Lamprophiidae"
    ),  # Missclassification
    **dict.fromkeys(
        [
            "Scolecomorphidae",
            "Herpelidae",
            "Indotyphlidae",
            "Dermophiidae",
            "Typhlonectidae",
            "Siphonopidae",
        ],
        "Caeciliidae",
    ),  # Missclassification
    **dict.fromkeys(
        ["Odontophrynidae", "Alsodidae"], "Cycloramphidae"
    ),  # missclassification (Alsodidae considered as subfamily and Odontophrynidae moved to Cycloramphidae)
    **dict.fromkeys(["Chydoridae", "Euphyllidae", "Daphniidae"], "Not assigned"),
    **dict.fromkeys(["Pontoporiidae", "Lipotidae"], "Iniidae"),  # Missclassification
    **dict.fromkeys(
        ["Strigopidae", "Nestoridae"], "Psittacidae"
    ),  # Missclassification in aves
    **dict.fromkeys(
        ["Rhysodidae", "Trachypachidae"], "Carabidae"
    ),  # Missclassification
    **dict.fromkeys(
        ["Vitreledonellidae", "Bolitaenidae"], "Amphitretidae"
    ),  # Missclassification in mollusca
    **dict.fromkeys(
        ["Batrachylidae", "Telmatobiinae"], "Ceratophryidae"
    ),  # Missclassification (Batrachylidae is subfamily)
}

all_family = {"family": {**family, **multi_family}}


##---------------- Order --------------##
order = {
    "Trochiliformes": "Apodiformes",  # synonym in Aves
    "Upupiformes": "Bucerotiformes",  # missclassification in Aves
    "Holocentriformes": "Beryciformes",  # missclassification in Actinopteri
    "Semionotiformes": "Lepisosteiformes",  # synonym in Actinopteri
    "Cetartiodactyla": "Artiodactyla",  # missclassification (Cetartiodactyla is clade)
    "Phasmatodea": "Phasmida",  # synonym in insecta
    "Unionoida": "Unionida",  # spelling/grammar error
    "Xiphosura": "Xiphosurida",  # spelling/grammar error
    "Veneroida ": "Venerida",  # spelling/grammar error
    "Sepioloida": "Sepiida",  # missclassification
    "Cycloneritimorpha": "Cycloneritida",  # amendment of order name
    "Arcoida": "Arcida",  # spelling/grammar error
    "Mytiloida": "Mytilida",  # spelling/grammar error
    "Eupulmonata": "Ellobiida",  # missclassification (Eupulmonata is superorder of Ellobiida))
    "Isoptera": "Blattodea",  # missclassification (Isoptera is suborder)
    "Ostreoida": "Ostreida",  # spelling/grammar error
    "Actinaria": "Actiniaria",  # spelling/grammar error
    "Euphasiacea": "Euphausiacea",  # spelling/grammar error
    "Pterocliformes": "Pteroclidiformes",  # spelling/grammar error
    "Cathartiformes": "Accipitriformes",  # missclassification
    "Pectinoida": "Pectinida",  # spelling/grammar error
    "Oribatida": "Sarcoptiformes",  # missclassification
    "Zoanthinaria": "Zoantharia",  # spelling/grammar error
    "Ceriantharia": "Penicillaria",  # missclassification
    "Crocodilia": "Crocodylia",
}


multi_order = {
    **dict.fromkeys(
        [
            "Acanthuriformes",
            "Anabantiformes",
            "Blenniiformes",
            "Carangiformes",
            "Centrarchiformes",
            "Chaetodontiformes",
            "CichliformesGobiiformes",
            "Kurtiformes",
            "Labriformes",
            "Lutjaniformes",
            "Spariformes",
        ],
        "Perciformes",
    ),  # Actinopteri
    **dict.fromkeys(
        [
            "Onychophora",
            "Hygrophila",
            "Allogastropoda",
            "Bathyteuthida",
            "Sorbeoconcha",
            "Idiosepiida",
            "Patellogastropoda",
            "Onychophora",
            "Nerillida",
            "Archaeopulmonata",
        ],
        "Not assigned",
    ),
}


all_order = {"order": {**order, **multi_order}}

##--------------- Save dictionaries ---------------##
with open(TAXON + "order.json", "w") as fp:
    json.dump(all_order, fp)

with open(TAXON + "family.json", "w") as fp:
    json.dump(all_family, fp)

with open(TAXON + "class.json", "w") as fp:
    json.dump(all_class, fp)
