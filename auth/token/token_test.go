package token

import "testing"

func TestCreateAndValidateToken(t *testing.T) {
	t.Parallel()

	assertToken := func(tokenString string, subject string, isAdmin bool, impersonator string) {
		t.Helper()

		token, err := ValidateToken(tokenString)
		if err != nil {
			t.Errorf("could not validate token: %s", err)
		}

		if token.Subject != subject {
			t.Errorf("Got subject %s, expected testing", token.Subject)
		}

		if token.IsAdmin != isAdmin {
			t.Errorf("Got IsAdmin as %t, expected %t", token.IsAdmin, isAdmin)
		}

		if token.Impersonator != impersonator {
			t.Errorf("Got impersonator as %s, expected empty", token.Impersonator)
		}
	}

	t.Run("as_normal_user", func(t *testing.T) {
		t.Parallel()

		tokenString, err := CreateToken("testing", false)
		if err != nil {
			t.Errorf("could not create token: %s", err)
		}

		assertToken(tokenString, "testing", false, "")
	})

	t.Run("as_admin_user", func(t *testing.T) {
		t.Parallel()

		tokenString, err := CreateToken("AdminUser", true)
		if err != nil {
			t.Errorf("could not create token: %s", err)
		}

		assertToken(tokenString, "AdminUser", true, "")
	})

	t.Run("as_impersonated_user", func(t *testing.T) {
		t.Parallel()

		tokenString, err := CreateTokenWithImpersonator("ImpersonatedUser", false, "bigbro")
		if err != nil {
			t.Errorf("could not create token: %s", err)
		}

		assertToken(tokenString, "ImpersonatedUser", false, "bigbro")
	})
}
