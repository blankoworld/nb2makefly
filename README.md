This documentation is in french. Please refer to the README.en.md one to see it in English.

## Installation

Pré-requis : python 2

L'installation est simple : il suffit de copier le fichier **nb2makefly.py** dans le répertoire racine de votre blog Nanoblogger.

## Utilisation

Pour cela, créez deux répertoires : 

   * src
   * db

Ensuite lancez nb2makefly de la manière suivante : 

    python nb2makefly.py

Cela va remplir les dossiers **src** et **db**.

**ATTENTION** : la configuration par défaut devrait suffire, il faut cependant changer la variable suivante pour donner l'adresse de votre site web : **nanoblogger_url** (Cf. la section "Configuration de nb2makefly").

## Configuration de nb2makefly

Dans le fichier **nb2makefly.py** sont contenus plusieurs variables de configuration, dont voici les noms et leur utilité : 

  * limit : donne le nombre d'article maximum à importer/traiter
  * nanoblogger_conf : nom du fichier de configuration de Nanoblogger
  * datadir : répertoire dans lequel sont contenus les billets de Nanoblogger
  * data\_ext : extension de ces fichiers
  * cat\_ext : extension des fichiers de base de données de Nanoblogger
  * nanoblogger\_url : adresse de votre site web final
  * extension : extension des billets Makefly
  * db\_ext : extension des méta-données Makefly
  * default\_type : type par défaut des billets dans Makefly
  * default\_tag : tag par défaut dans Makefly si aucun trouvé dans Nanoblogger
  * default\_url : adresse par défaut pour Makefly
  * targetdir : répertoire cible pour le contenu des billets
  * dbtargetdir : répertoire cible pour les méta-données d'un billet
  * url\_replacement\_dict : contient une liste d'adresses à modifier, par exemple pour changer tout les */joueb/* en l'adresse contenu par la variable *default_url*, on met : 

    {
       '/joueb/': default_url,
    }

## Anciens liens de Nanoblogger et redirection

Pour rediriger les anciens liens de Nanoblogger vers Makefly, sur votre serveur web (Apache2) utilisez la redirection permanente.

    Redirect permanent /ancienlien http://monsite.tld/nouveau_lien

> Comment avoir la liste des anciens liens ?

Il suffit d'aller dans le répertoire archives dans votre dossier Nanoblogger, puis de faire un `ls -R`.
