from django import forms


class GenerateShopForm(forms.Form):
    name = forms.CharField()

    # Equipment fields

    # Equipment common
    equipment_common_min = forms.IntegerField()
    equipment_common_max = forms.IntegerField()
    equipment_common_allow_duplicates = forms.BooleanField()

    # Equipment uncommon
    equipment_uncommon_min = forms.IntegerField()
    equipment_uncommon_max = forms.IntegerField()
    equipment_uncommon_allow_duplicates = forms.BooleanField()

    # Equipment rare
    equipment_rare_min = forms.IntegerField()
    equipment_rare_max = forms.IntegerField()
    equipment_rare_allow_duplicates = forms.BooleanField()

    # Equipment very rare
    equipment_very_rare_min = forms.IntegerField()
    equipment_very_rare_max = forms.IntegerField()
    equipment_very_rare_allow_duplicates = forms.BooleanField()

    # Equipment legendary
    equipment_legendary_min = forms.IntegerField()
    equipment_legendary_max = forms.IntegerField()
    equipment_legendary_allow_duplicates = forms.BooleanField()

    # Magical Item Fields

    # Magical Item common
    magic_item_common_min = forms.IntegerField()
    magic_item_common_max = forms.IntegerField()
    magic_item_common_allow_duplicates = forms.BooleanField()

    # Magical Item uncommon
    magic_item_uncommon_min = forms.IntegerField()
    magic_item_uncommon_max = forms.IntegerField()
    magic_item_uncommon_allow_duplicates = forms.BooleanField()

    # Magical Item rare
    magic_item_rare_min = forms.IntegerField()
    magic_item_rare_max = forms.IntegerField()
    magic_item_rare_allow_duplicates = forms.BooleanField()

    # Magical Item very rare
    magic_item_very_rare_min = forms.IntegerField()
    magic_item_very_rare_max = forms.IntegerField()
    magic_item_very_rare_allow_duplicates = forms.BooleanField()

    # Magical Item legendary
    magic_item_legendary_min = forms.IntegerField()
    magic_item_legendary_max = forms.IntegerField()
    magic_item_legendary_allow_duplicates = forms.BooleanField()

    # Potions fields

    # Potion items common
    potion_common_min = forms.IntegerField()
    potion_common_max = forms.IntegerField()
    potion_common_allow_duplicates = forms.BooleanField()

    # Potion items uncommon
    potion_uncommon_min = forms.IntegerField()
    potion_uncommon_max = forms.IntegerField()
    potion_uncommon_allow_duplicates = forms.BooleanField()

    # Potion items rare
    potion_rare_min = forms.IntegerField()
    potion_rare_max = forms.IntegerField()
    potion_rare_allow_duplicates = forms.BooleanField()

    # Potion items very rare
    potion_very_rare_min = forms.IntegerField()
    potion_very_rare_max = forms.IntegerField()
    potion_very_rare_allow_duplicates = forms.BooleanField()

    # Potion items legendary
    potion_legendary_min = forms.IntegerField()
    potion_legendary_max = forms.IntegerField()
    potion_legendary_allow_duplicates = forms.BooleanField()

    # Spells fields

    # Spell scrolls cantrips

    spell_cantrip_min = forms.IntegerField()
    spell_cantrip_max = forms.IntegerField()
    spell_cantrip_allow_duplicates = forms.BooleanField()

    # Spell scrolls level one
    spell_level_one_min = forms.IntegerField()
    spell_level_one_max = forms.IntegerField()
    spell_level_one_allow_duplicates = forms.BooleanField()

    # Spell scrolls level two
    spell_level_two_min = forms.IntegerField()
    spell_level_two_max = forms.IntegerField()
    spell_level_two_allow_duplicates = forms.BooleanField()

    # Spell scrolls level three
    spell_level_three_min = forms.IntegerField()
    spell_level_three_max = forms.IntegerField()
    spell_level_three_allow_duplicates = forms.BooleanField()

    # Spell scrolls level four
    spell_level_four_min = forms.IntegerField()
    spell_level_four_max = forms.IntegerField()
    spell_level_four_allow_duplicates = forms.BooleanField()

    # Spell scrolls level five
    spell_level_five_min = forms.IntegerField()
    spell_level_five_max = forms.IntegerField()
    spell_level_five_allow_duplicates = forms.BooleanField()

    # Spell scrolls level six
    spell_level_six_min = forms.IntegerField()
    spell_level_six_max = forms.IntegerField()
    spell_level_six_allow_duplicates = forms.BooleanField()

    # Spell scrolls level seven
    spell_level_seven_min = forms.IntegerField()
    spell_level_seven_max = forms.IntegerField()
    spell_level_seven_allow_duplicates = forms.BooleanField()

    # Spell scrolls level eight
    spell_level_eight_min = forms.IntegerField()
    spell_level_eight_max = forms.IntegerField()
    spell_level_eight_allow_duplicates = forms.BooleanField()

    # Spell scrolls level nine
    spell_level_nine_min = forms.IntegerField()
    spell_level_nine_max = forms.IntegerField()
    spell_level_nine_allow_duplicates = forms.BooleanField()
