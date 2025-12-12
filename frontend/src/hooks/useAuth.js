import { useState, useEffect } from 'react';
import { getProfile } from '../api/userService';

export function useAuth() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('access');
      if (!token) {
        setUser(null);
        setLoading(false);
        return;
      }

      try {
        const { data } = await getProfile();
        setUser(data);
      } catch (error) {
        localStorage.removeItem('access');
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const logout = () => {
    localStorage.clear();
    setUser(null);
    window.location.href = '/login';
  };

  const getDisplayName = () => {
    if (!user) return '';
    if (user.first_name && user.last_name) {
      return `${user.first_name} ${user.last_name}`;
    }
    if (user.first_name) {
      return user.first_name;
    }
    return user.username;
  };

  return {
    user,
    loading,
    logout,
    isAuthenticated: !!user,
    displayName: getDisplayName(),
    isStaff: user?.is_staff || false
  };
}
