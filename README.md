# RuDSI: Word sense induction (WSI) dataset for Russian

RuDSI is a new benchmark for word sense induction (WSI) in Russian.
The dataset was created using manual annotation and semi-automatic clustering of Word Usage Graphs (WUGs).
Unlike prior WSI datasets for Russian, RuDSI is completely data-driven (based on texts from Russian National Corpus), with no external word senses imposed on annotators.
Depending on the parameters of graph clustering, different derivative datasets can be produced from raw annotation.

Inter-rater agreement: 0.41 as measured by Krippendorff's alpha.

# Paper

[`RuDSI: graph-based word sense induction dataset for Russian`](https://aclanthology.org/2022.textgraphs-1.9/) by Anna Aksenova, Ekaterina Gavrishina, Elisey Rykov and Andrey Kutuzov (2022)


## Files and directories
* `rudsi_russe18.tsv`: RuDSI in the RUSSE'18 format.
* `annotation/`: scripts to prepare data for the annotation
* `data/`: words and their contexts (sentences) annotated by the annotators
* `data_join/`: all annotators' judgments in one file
* `clusters/`: clusters (senses) automatically assigned to word usages
* `graphs/`: word usage graphs in the NetworkX format
* `plots/`: visualized graphs in HTML
* `stats/`: various statistics about RuDSI

![Word usage graph example](graph_example.png?raw=true "Word usage graph example")

