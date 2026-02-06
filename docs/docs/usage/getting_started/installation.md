---
slug: /installation
title: Installation
sidebar_position: 2
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Install PyMUSAS

Can be installed on all operating systems and supports Python version >= `3.10` and < `3.14`, to install run:

``` bash
pip install pymusas
```

:::note
PyMUSAS can be installed on Python 3.14 but we do not advise it, as pipeline models downloaded from spaCy like [`en_core_web_sm`](https://spacy.io/models/en) fail to install due to it requiring pydnatic version 1 which currently does not support Python version 3.14. For more details on this see the following [issue](https://github.com/UCREL/pymusas/issues/57) on the PyMUSAS GitHub repository.
:::


## Install for Neural or Hybrid Taggers

If you would like to use the Neural or Hybrid taggers the `neural` extra is required:

:::note
this will install the default version of [PyTorch](https://pytorch.org/) for your operating system if you would like to use a specific version of PyTorch, e.g. CUDA, AMD GPU, etc please install the specific version of `torch` first and then `pymusas[neural]`.

:::

<Tabs groupId="shell-choice">
<TabItem value="bash" label="bash">

``` bash
pip install pymusas[neural]
```

</TabItem>
<TabItem value="zsh" label="zsh">

``` bash
pip install 'pymusas[neural]'
```

</TabItem>
</Tabs>
