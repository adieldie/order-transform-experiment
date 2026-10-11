# Order transform experiment

**Estágio: experimental / em teste. Demonstração parcial sanitizada, não pronta para produção.**

Experimental selected-source snapshot of an order automation project. This is not the complete robot or an independently finished application.

## Included
- Original helper formatting product quantity changes.
- Original text/area normalization helpers.
- Original ISO timestamp parsing helper.

The selected function bodies are unchanged. Imports were added so the helpers can be inspected separately. No configuration, production endpoints, customers, credentials, databases, logs, browser sessions or source history is included.

## Stage and known limitations
Experimental / incomplete. The original larger source has a syntax error in its execution region. That region is excluded, not repaired. This excerpt does not establish that the complete source runs.

The date helper returns datetime inputs unchanged, but converts timezone-aware strings to a fixed UTC-03 offset and strips timezone information. Naive strings are assumed to be UTC. These inconsistent input semantics are deliberately retained. The area normalizer removes digits and can collapse distinct names. No corrective changes were made.

## Inspect and try
Python 3.10 or newer; standard library only. An optional synthetic example:

```python
from order_helpers import formatar_info_edicao
print(formatar_info_edicao({
    "items": [{"variantId": "sample-1", "name": "Item fictício"}],
    "productChangesHistory": [{"originalVariantId": "sample-1", "originalQuantity": 1, "finalQuantity": 2}]
}))
```

No runtime tests or production integration tests were run for this snapshot. This is a source-study artifact, not a certified runnable system. No license grant has been invented; redistribution terms remain to be defined by the rights holder.
