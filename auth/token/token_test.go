package token

import "testing"

func TestCreateToken(t *testing.T) {
	t.Parallel()

	tokenString, err := CreateToken("testing", false)

	if err != nil {
		t.Errorf("could not create token: %s", err)
	}

	token, err := ValidateToken(tokenString)

	if err != nil {
		t.Errorf("could not validate token: %s", err)
	}

	if token.Subject != "testing" {
		t.Errorf("Got subject %s, expected testing", token.Subject)
	}

	if token.IsAdmin {
		t.Error("Got IsAdmin as true, expected false")
	}

	if token.Impersonator != "" {
		t.Errorf("Got impersonator as %s, expected empty", token.Impersonator)
	}
}
