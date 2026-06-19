import random

from core.entities.battle import BattlePokemonMove
from core.entities.moves import (
    AilmentEnum,
    CategoryEnum,
    DamageClassEnum,
    MoveAilment,
    MoveHits,
    MoveTurns,
    PokemonMove,
    TargetEnum,
)
from core.entities.pokemon import Pokemon, PokemonMoveMetadata, PokemonStats
from core.entities.types import PokemonType
from core.services.move_selector import MoveSelector


def make_type(key: str) -> PokemonType:
    return PokemonType(
        id=1,
        key=key,
        name=key.title(),
        double_damage_from=[],
        double_damage_to=[],
        half_damage_from=[],
        half_damage_to=[],
        no_damage_from=[],
        no_damage_to=[],
    )


def make_stats(attack: int = 50, sp_attack: int = 50, **kwargs) -> PokemonStats:
    defaults = dict(hp=50, attack=attack, defense=50, sp_attack=sp_attack, sp_defense=50, speed=50)
    defaults.update(kwargs)
    return PokemonStats(**defaults)


def make_move(
    *,
    name: str,
    type_key: str = "normal",
    damage_class: DamageClassEnum = DamageClassEnum.PHYSICAL,
    power: int | None = 40,
    accuracy: int | None = 100,
    pp: int | None = 20,
    priority: int = 0,
    category: CategoryEnum = CategoryEnum.DAMAGE,
) -> PokemonMove:
    return PokemonMove(
        id=hash(name) & 0xFFFF,
        key=name.lower().replace(" ", "-"),
        name=name,
        type=make_type(type_key),
        damage_class=damage_class,
        power=power,
        accuracy=accuracy,
        pp=pp,
        priority=priority,
        target=TargetEnum.SELECTED_POKEMON,
        category=category,
        crit_rate=0,
        drain=0,
        flinch_chance=0,
        healing=0,
        ailment_data=MoveAilment(ailment=AilmentEnum.NONE, chance=0),
        hits_limit=MoveHits(max_hits=None, min_hits=None),
        turns_limit=MoveTurns(max_turns=None, min_turns=None),
        stat_changes=[],
    )


def make_metadata(move: PokemonMove, level: int = 0) -> PokemonMoveMetadata:
    return PokemonMoveMetadata(level_learned_at=level, move=move)


def make_pokemon(
    *,
    name: str = "mon",
    type_keys: tuple[str, ...] = ("normal",),
    stats: PokemonStats | None = None,
    moves_metadata: list[PokemonMoveMetadata] | None = None,
) -> Pokemon:
    return Pokemon(
        id=1,
        key=name.lower(),
        name=name,
        base_experience=50,
        stats=stats or make_stats(),
        types=[make_type(k) for k in type_keys],
        moves_metadata=moves_metadata or [],
        color="white",
    )


def test_returns_empty_tuple_when_no_moves():
    pokemon = make_pokemon()
    assert MoveSelector().select(pokemon) == ()


def test_short_circuits_when_four_or_fewer_moves_without_calling_rng():
    moves = [make_metadata(make_move(name=f"move-{i}", power=40, pp=20)) for i in range(4)]
    pokemon = make_pokemon(moves_metadata=moves)

    rng = random.Random(0)
    original_state = rng.getstate()
    selected = MoveSelector(rng=rng).select(pokemon)
    assert rng.getstate() == original_state, "RNG was consumed despite ≤4 candidates"
    assert len(selected) == 4
    assert [m.move.name for m in selected] == [f"move-{i}" for i in range(4)]


def test_returns_all_moves_unchanged_when_four_or_fewer():
    moves = [
        make_metadata(make_move(name="bad", power=None)),
        make_metadata(make_move(name="good", type_key="fire", power=90)),
    ]
    pokemon = make_pokemon(type_keys=("fire",), moves_metadata=moves)
    selected = MoveSelector().select(pokemon)
    assert {m.move.name for m in selected} == {"bad", "good"}


def test_returns_at_most_four_moves():
    moves = [make_metadata(make_move(name=f"move-{i}")) for i in range(10)]
    pokemon = make_pokemon(moves_metadata=moves)
    selected = MoveSelector().select(pokemon)
    assert len(selected) == 4
    assert all(isinstance(m, BattlePokemonMove) for m in selected)


def test_returns_all_moves_when_pokemon_has_fewer_than_four():
    moves = [make_metadata(make_move(name="splash")) for _ in range(2)]
    pokemon = make_pokemon(name="magikarp", type_keys=("water",), moves_metadata=moves)
    selected = MoveSelector().select(pokemon)
    assert len(selected) == 2
    assert {m.move.name for m in selected} == {"splash"}


def test_each_selected_move_has_positive_pp():
    moves = [make_metadata(make_move(name=f"move-{i}", pp=10)) for i in range(8)]
    pokemon = make_pokemon(moves_metadata=moves)
    for move in MoveSelector().select(pokemon):
        assert move.current_pp > 0


def test_stab_move_outranks_non_stab_of_same_power():
    stab = make_metadata(make_move(name="thunder-shock", type_key="electric", power=40))
    non_stab = make_metadata(make_move(name="mega-punch", type_key="normal", power=40))
    filler = make_metadata(make_move(name="growl", power=None, pp=40))
    pokemon = make_pokemon(
        type_keys=("electric",),
        stats=make_stats(sp_attack=100),
        moves_metadata=[stab, non_stab, filler, filler, filler],
    )
    selected = MoveSelector(rng=random.Random(0)).select(pokemon)
    names = {m.move.name for m in selected}
    assert "thunder-shock" in names
    assert "mega-punch" not in names


def test_high_power_stab_beats_low_power_stab():
    thunderbolt = make_metadata(make_move(name="thunderbolt", type_key="electric", power=90))
    thunder_shock = make_metadata(make_move(name="thunder-shock", type_key="electric", power=40))
    filler = make_metadata(make_move(name="growl", power=None, pp=40))
    pokemon = make_pokemon(
        type_keys=("electric",),
        stats=make_stats(sp_attack=100),
        moves_metadata=[thunder_shock, thunderbolt, filler, filler, filler],
    )
    selected = MoveSelector(rng=random.Random(0)).select(pokemon)
    names = {m.move.name for m in selected}
    assert "thunderbolt" in names


def test_class_match_bonus_picks_special_when_special_attack_higher():
    special_move = make_metadata(
        make_move(
            name="psychic",
            type_key="psychic",
            damage_class=DamageClassEnum.SPECIAL,
            power=90,
        )
    )
    physical_move = make_metadata(
        make_move(
            name="tackle",
            type_key="normal",
            damage_class=DamageClassEnum.PHYSICAL,
            power=90,
        )
    )
    pokemon = make_pokemon(
        type_keys=("psychic",),
        stats=make_stats(attack=40, sp_attack=120),
        moves_metadata=[physical_move, special_move],
    )
    selected = MoveSelector(rng=random.Random(0)).select(pokemon)
    names = {m.move.name for m in selected}
    assert "psychic" in names


def test_high_level_moves_are_penalized_relative_to_equivalent_low_level_move():
    pokemon = make_pokemon(
        moves_metadata=[
            make_metadata(make_move(name="low-power-low-level", power=80, pp=20), level=1),
            make_metadata(make_move(name="low-power-high-level", power=80, pp=20), level=60),
        ]
    )
    sel = MoveSelector()
    low_score = sel._score(pokemon.moves_metadata[0], pokemon).score
    high_score = sel._score(pokemon.moves_metadata[1], pokemon).score
    assert low_score > high_score
    assert high_score < low_score


def test_bad_moves_are_filtered_out_by_tier():
    good_move = make_metadata(make_move(name="thunderbolt", type_key="electric", power=90, pp=15))
    bad_move = make_metadata(make_move(name="mega-punch", type_key="normal", power=80, pp=20))
    pokemon = make_pokemon(
        type_keys=("electric",),
        stats=make_stats(sp_attack=100),
        moves_metadata=[good_move, bad_move],
    )
    runs = [MoveSelector(rng=random.Random(seed)).select(pokemon) for seed in range(20)]
    for selected in runs:
        names = {m.move.name for m in selected}
        assert "thunderbolt" in names


def test_randomness_produces_variation_across_runs():
    moves = [
        make_metadata(
            make_move(
                name=f"move-{i}",
                type_key="electric",
                power=80,
                pp=15,
                damage_class=DamageClassEnum.SPECIAL,
            )
        )
        for i in range(10)
    ]
    pokemon = make_pokemon(type_keys=("electric",), stats=make_stats(sp_attack=100), moves_metadata=moves)
    runs = [tuple(sorted(m.move.name for m in MoveSelector().select(pokemon))) for _ in range(10)]
    assert len(set(runs)) > 1, "Expected variation across RNG runs but got identical outputs"


def test_is_deterministic_with_same_seed():
    moves = [
        make_metadata(
            make_move(
                name=f"move-{i}",
                type_key="fire",
                power=80,
                pp=15,
                damage_class=DamageClassEnum.SPECIAL,
            )
        )
        for i in range(10)
    ]
    pokemon = make_pokemon(type_keys=("fire",), stats=make_stats(sp_attack=100), moves_metadata=moves)
    a = tuple(m.move.name for m in MoveSelector(rng=random.Random(42)).select(pokemon))
    b = tuple(m.move.name for m in MoveSelector(rng=random.Random(42)).select(pokemon))
    assert a == b


def test_different_seeds_produce_different_results_eventually():
    moves = [
        make_metadata(
            make_move(
                name=f"move-{i}",
                type_key="water",
                power=80,
                pp=15,
                damage_class=DamageClassEnum.SPECIAL,
            )
        )
        for i in range(10)
    ]
    pokemon = make_pokemon(type_keys=("water",), stats=make_stats(sp_attack=100), moves_metadata=moves)
    outputs = {
        tuple(m.move.name for m in MoveSelector(rng=random.Random(seed)).select(pokemon))
        for seed in range(30)
    }
    assert len(outputs) > 1


def test_real_pikachu_picks_stab_moves():
    from core.repositories import PokemonRepository

    PokemonRepository.clear_cache()
    pikachu = PokemonRepository.get("pikachu")
    selected = MoveSelector(rng=random.Random(7)).select(pikachu)
    assert len(selected) == 4
    electric_count = sum(1 for m in selected if m.move.type.key == "electric")
    assert electric_count >= 1, f"Pikachu got no Electric moves: {[m.move.name for m in selected]}"
    pkmn_type_keys = {t.key for t in pikachu.types}
    non_stab = [m.move.name for m in selected if m.move.type.key not in pkmn_type_keys]
    assert len(non_stab) <= 2, f"Pikachu has too many non-STAB moves: {non_stab}"


def test_real_magikarp_returns_all_moves():
    from core.repositories import PokemonRepository

    PokemonRepository.clear_cache()
    magikarp = PokemonRepository.get("magikarp")
    selected = MoveSelector(rng=random.Random(0)).select(magikarp)
    assert 1 <= len(selected) <= 4
    assert all(m.current_pp > 0 for m in selected)
