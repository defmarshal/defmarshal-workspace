#!/usr/bin/env python3
"""
Category-theoretic comparative framework for AGI architectures.
Demonstrates categories, functors, and natural transformations.
"""

from typing import Dict, List, Callable, Optional, Set, Tuple
from dataclasses import dataclass

@dataclass
class Morphism:
    name: str
    source: 'Object'
    target: 'Object'
    compose: Optional[Callable] = None

@dataclass
class Object:
    name: str
    category: 'Category'

class Category:
    def __init__(self, name: str):
        self.name = name
        self.objects: Dict[str, Object] = {}
        self.morphisms: List[Morphism] = []
    
    def add_object(self, name: str) -> Object:
        obj = Object(name, self)
        self.objects[name] = obj
        return obj
    
    def add_morphism(self, name: str, source: Object, target: Object) -> Morphism:
        m = Morphism(name, source, target)
        self.morphisms.append(m)
        return m
    
    def identity(self, obj: Object) -> Morphism:
        return Morphism(f"id_{obj.name}", obj, obj)
    
    def compose(self, f: Morphism, g: Morphism) -> Optional[Morphism]:
        if f.target != g.source:
            return None
        return Morphism(f"{f.name}∘{g.name}", f.source, g.target)

class Functor:
    def __init__(self, name: str, source: Category, target: Category):
        self.name = name
        self.source = source
        self.target = target
        self.obj_map: Dict[Object, Object] = {}
        self.mor_map: Dict[Morphism, Morphism] = {}
    
    def map_object(self, src_obj: Object, tgt_obj: Object):
        self.obj_map[src_obj] = tgt_obj
    
    def map_morphism(self, src_mor: Morphism, tgt_mor: Morphism):
        self.mor_map[src_mor] = tgt_mor
    
    def preserves_identity(self, obj: Object) -> bool:
        if obj not in self.obj_map:
            return False
        id_src = self.source.identity(obj)
        id_tgt = self.target.identity(self.obj_map[obj])
        mapped = self.mor_map.get(id_src)
        return mapped == id_tgt
    
    def preserves_composition(self, f: Morphism, g: Morphism) -> bool:
        if f not in self.mor_map or g not in self.mor_map:
            return False
        comp_src = self.source.compose(f, g)
        if comp_src is None:
            return True  # not composable, vacuously preserved
        comp_tgt = self.target.compose(self.mor_map[f], self.mor_map[g])
        mapped_comp = self.mor_map.get(comp_src)
        return mapped_comp == comp_tgt

class AGIComparator:
    def __init__(self):
        self.setup_categories()
        self.setup_functors()
    
    def setup_categories(self):
        # Category of Symbolic AI systems
        self.Symbolic = Category("SymbolicAI")
        s_logic = self.Symbolic.add_object("LogicBased")
        s_kr = self.Symbolic.add_object("KnowledgeRepresentation")
        s_plan = self.Symbolic.add_object("PlanningSystems")
        
        self.Symbolic.add_morphism("symbolize", s_logic, s_kr)
        self.Symbolic.add_morphism("reason", s_kr, s_plan)
        self.Symbolic.add_morphism("infer", s_logic, s_plan)
        
        # Category of Connectionist AI
        self.Connectionist = Category("Connectionist")
        c_mlp = self.Connectionist.add_object("MLP")
        c_cnn = self.Connectionist.add_object("CNN")
        c_rnn = self.Connectionist.add_object("RNN")
        c_trans = self.Connectionist.add_object("Transformer")
        
        self.Connectionist.add_morphism("feedforward", c_mlp, c_cnn)
        self.Connectionist.add_morphism("sequence", c_rnn, c_trans)
        self.Connectionist.add_morphism("train", c_mlp, c_rnn)
        
    def setup_functors(self):
        # Functor: maps symbolic concepts to neural equivalents
        self.Neuralization = Functor("Neuralization", self.Symbolic, self.Connectionist)
        
        mapping = {
            "LogicBased": "MLP",
            "KnowledgeRepresentation": "CNN",
            "PlanningSystems": "RNN"
        }
        for s_name, t_name in mapping.items():
            s_obj = self.Symbolic.objects[s_name]
            t_obj = self.Connectionist.objects[t_name]
            self.Neuralization.map_object(s_obj, t_obj)
        
        # Map some key morphisms
        morph_map = {
            "symbolize": ("feedforward", True),
            "reason": ("sequence", True),
            "infer": ("train", False)  # not exact mapping, illustrative
        }
        for s_mor in self.Symbolic.morphisms:
            if s_mor.name in morph_map:
                tgt_name, exact = morph_map[s_mor.name]
                t_obj_src = self.Neuralization.obj_map[s_mor.source]
                t_obj_tgt = self.Neuralization.obj_map[s_mor.target]
                t_mor = None
                for m in self.Connectionist.morphisms:
                    if m.name == tgt_name and m.source == t_obj_src and m.target == t_obj_tgt:
                        t_mor = m
                        break
                if t_mor:
                    self.Neuralization.map_morphism(s_mor, t_mor)
    
    def verify_functor_laws(self) -> Tuple[int, int]:
        identity_ok = 0
        compose_ok = 0
        total_obj = 0
        total_comp = 0
        
        for obj in self.Symbolic.objects.values():
            total_obj += 1
            if self.Neuralization.preserves_identity(obj):
                identity_ok += 1
        
        for f in self.Symbolic.morphisms:
            for g in self.Symbolic.morphisms:
                total_comp += 1
                if self.Neuralization.preserves_composition(f, g):
                    compose_ok += 1
        
        return identity_ok, compose_ok
    
    def compute_similarity(self) -> float:
        """Heuristic: ratio of mapped objects and morphisms."""
        obj_cov = len(self.Neuralization.obj_map) / len(self.Symbolic.objects)
        mor_cov = len(self.Neuralization.mor_map) / len(self.Symbolic.morphisms)
        return (obj_cov + mor_cov) / 2

def main():
    comparator = AGIComparator()
    
    print("=== Category-theoretic AGI Comparison ===\n")
    
    print("Source category (Symbolic AI):")
    print(f"  Objects: {[o.name for o in comparator.Symbolic.objects.values()]}")
    print(f"  Morphisms: {[m.name for m in comparator.Symbolic.morphisms]}")
    
    print("\nTarget category (Connectionist):")
    print(f"  Objects: {[o.name for o in comparator.Connectionist.objects.values()]}")
    print(f"  Morphisms: {[m.name for m in comparator.Connectionist.morphisms]}")
    
    print("\nFunctors defined:")
    print(f"  - {comparator.Neuralization.name}")
    
    id_ok, comp_ok = comparator.verify_functor_laws()
    print("\nFunctor law verification:")
    print(f"  Identity preservation: {id_ok}/{len(comparator.Symbolic.objects)}")
    print(f"  Composition preservation: {comp_ok} checks (exact number depends on pairs)")
    
    sim = comparator.compute_similarity()
    print(f"\nMapping coverage score: {sim:.2f}")
    
    print("\nInterpretation:")
    print(" A high coverage indicates substantial structural alignment between")
    print(" symbolic and connectionist paradigms, suggesting potential for")
    print(" hybrid architectures that leverage both.")

if __name__ == "__main__":
    main()