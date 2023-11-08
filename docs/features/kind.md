---
title: `kind`
---

**clause kind**


This feature is present on objects of type
[`clause`](otype.md).

##### Note
> In version 4 this feature was called `clause_kind`.

This feature divides the clauses into three types: *verbal*, *nominal* and *without predication*.
It is related to the feature [`typ`](typ.md) on clauses, in the sense that each of the values of `kind` 
corresponds to a set of values of `typ`.

So, this is essentially a feature for convenience: it leads to more concise queries of which the intention is also clearer.

value |meaning | correspondence with `typ` values on *clauses*
---|---|---
`VC`|Verbal clauses | `InfA` `InfC` `Ptcp` `Way0` `WayX` `WIm0` `WImX` `WQt0` `WQtX` `WxI0` `WXIm` `WxIX` `WxQ0` `WXQt` `WxQX` `WxY0` `WXYq` `WxYX` `WYq0` `WYqX` `xIm0` `XImp` `xImX` `xQt0` `XQtl` `xQtX` `xYq0` `XYqt` `xYqX` `ZIm0` `ZImX` `ZQt0` `ZQtX` `ZYq0` `ZYqX`
`NC`|Nominal clauses | `AjCl` `NmCl`
`WP`|Clauses without predication| `CPen` `Ellp` `MSyn` `Reop` `Voct` `XPos`

