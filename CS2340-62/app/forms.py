from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, SelectField
from wtforms.validators import InputRequired, ValidationError
from app.entities import User, Region


class Travel(FlaskForm):
    submit = SubmitField('Travel')


class CreateUserForm(FlaskForm):
    name = StringField('Player Name:', validators=[InputRequired()], default="")
    pilot_skill = HiddenField('Pilot Skill', validators=[InputRequired()], default="0")
    fighter_skill = HiddenField('Fighter Skill', validators=[InputRequired()], default="0")
    merchant_skill = HiddenField('Merchant Skill', validators=[InputRequired()], default="0")
    engineer_skill = HiddenField('Engineer Skill', validators=[InputRequired()], default="0")
    difficulty = SelectField('Difficulty:',
                             choices=[('easy', 'Easy (max 16 points)'), ('medium', 'Medium (max 12 points)'),
                                      ('hard', 'Hard (max 8 points)')], validators=[InputRequired()])
    submit = SubmitField('Create Character')

    def set_p_skill(self, value):
        self.pilot_skill.value = value

    def validate(self):
        print("is type valid: " + str(self.restrict_type()))
        # print("is difficulty valid: " + str(self.restrict_difficulty()))
        is_valid = self.restrict_type()
        return is_valid

    def restrict_type(self):
        print("validating the restrict type")
        if not str(self.name.data).isalpha():
            return False
            raise ValidationError("You need to enter letters (A-Z) here.")
        if not str(self.pilot_skill.data).isdigit():
            return False
            raise ValidationError("You need to enter a number here.")
        if not str(self.fighter_skill.data).isdigit():
            return False
            raise ValidationError("You need to enter a number here.")
        if not str(self.merchant_skill.data).isdigit():
            return False
            raise ValidationError("You need to enter a number here.")
        if not str(self.engineer_skill.data).isdigit():
            return False
            raise ValidationError("You need to enter a number here.")
        return True
