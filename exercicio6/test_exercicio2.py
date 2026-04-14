def access_control(is_admin, is_owner, is_public, is_logged_in):
    return (is_admin or is_owner) and (is_public or is_logged_in)

## FFVF
def test_not_admin_not_owner_public_not_logged_in():
    assert access_control(False, False, True, False) == False

## VFVF
def test_admin_not_owner_public_not_logged_in():
    assert access_control(True, False, True, False) == True

## FVFV
def test_not_admin_owner_public_not_logged_in():
    assert access_control(False, True, True, False) == True
    
## VFFF
def test_admin_not_owner_not_public_not_logged_in():
    assert access_control(True, False, False, False) == False
    
## VFFV
def test_admin_not_owner_not_public_logged_in():
    assert access_control(True, False, False, True) == True
