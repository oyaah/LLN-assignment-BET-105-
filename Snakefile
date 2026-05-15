configfile: "config.yaml"

N = config["n"]
K_VALUES = config["k_values"]
REPEATS = config["repeats"]

rule all:
    input:
        "plots/lln_plot.png"

rule simulate:
    output:
        "results/k_{k}.tsv"
    params:
        n = N,
        repeats = REPEATS
    shell:
        "python3 scripts/simulate.py {params.n} {wildcards.k} {params.repeats} {output}"

rule plot:
    input:
        expand("results/k_{k}.tsv", k=K_VALUES)
    output:
        "plots/lln_plot.png"
    params:
        n = N
    shell:
        "python3 scripts/plot.py results {params.n} {output}"
