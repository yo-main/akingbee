#[derive(Debug, Default)]
pub struct Permissions {
    pub impersonate: bool,
}

impl Permissions {
    pub fn new() -> Self {
        Permissions { impersonate: false }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn new_permissions() {
        let permission = Permissions::new();
        assert_eq!(permission.impersonate, false);
    }
}
