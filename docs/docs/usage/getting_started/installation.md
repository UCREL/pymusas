---
slug: /installation
title: Installation
sidebar_position: 2
---

# Install PyMUSAS

Can be installed on all operating systems and supports Python version >= `3.10` and < `3.15`, to install run:

``` bash
pip install pymusas
```


## Install for Neural or Hybrid models

If you would like to use the Neural or Hybrid models the `neural` extra is required:

:::note
this will install the default version of [PyTorch](https://pytorch.org/) for your operating system if you would like to use a specific version of PyTorch, e.g. CUDA, AMD GPU, etc please install the specific version of `torch` first and then `pymusas[neural]`.

:::

``` bash
pip install pymusas[neural]
```