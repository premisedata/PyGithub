############################ Copyrights and license ############################
#                                                                              #
# Copyright 2023 Mauricio Martinez <mauricio.martinez@premise.com>             #
#                                                                              #
# This file is part of PyGithub.                                               #
# http://pygithub.readthedocs.io/                                              #
#                                                                              #
# PyGithub is free software: you can redistribute it and/or modify it under    #
# the terms of the GNU Lesser General Public License as published by the Free  #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# PyGithub is distributed in the hope that it will be useful, but WITHOUT ANY  #
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS    #
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more #
# details.                                                                     #
#                                                                              #
# You should have received a copy of the GNU Lesser General Public License     #
# along with PyGithub. If not, see <http://www.gnu.org/licenses/>.             #
#                                                                              #
################################################################################

from github import Secret
from github.GithubObject import NotSet
from github.PaginatedList import PaginatedList
from github.Repository import Repository


class OrganizationSecret(Secret):
    """
    This class represents a org level GitHub secret. The reference can be found here https://docs.github.com/en/rest/actions/secrets
    """

    @property
    def visibility(self):
        """
        :type: string
        """
        self._completeIfNotSet(self._visibility)
        return self._visibility.value

    @property
    def selected_repositories(self) -> PaginatedList[Repository]:
        return PaginatedList(
            Repository,
            self._requester,
            self._selected_repositories_url,
            {},
            list_item="repositories",
        )

    def add_repo(self, repo: Repository) -> bool:
        """
        :calls: 'PUT {org_url}/actions/secrets/{secret_name} <https://docs.github.com/en/rest/actions/secrets#add-selected-repository-to-an-organization-secret>`_
        :param repo: github.Repository.Repository
        :rtype: bool
        """
        if self.visibility != "selected":
            return False
        self._requester.requestJsonAndCheck("PUT", f"{self.url}/repositories/{repo.id}")
        self._selected_repositories.value.append(repo)
        return True

    def remove_repo(self, repo: Repository) -> bool:
        """
        :calls: 'DELETE {org_url}/actions/secrets/{secret_name} <https://docs.github.com/en/rest/actions/secrets#add-selected-repository-to-an-organization-secret>`_
        :param repo: github.Repository.Repository
        :rtype: bool
        """
        if self.visibility != "selected":
            return False
        self._requester.requestJsonAndCheck("DELETE", f"{self.url}/repositories/{repo.id}")
        self._selected_repositories.value.remove(repo)
        return True

    def _initAttributes(self):
        self._name = NotSet
        self._created_at = NotSet
        self._updated_at = NotSet
        self._visibility = NotSet
        self._selected_repositories = NotSet
        self._selected_repositories_url = NotSet
        self._url = NotSet

    def _useAttributes(self, attributes):
        if "name" in attributes:
            self._name = self._makeStringAttribute(attributes["name"])
        if "created_at" in attributes:
            self._created_at = self._makeDatetimeAttribute(attributes["created_at"])
        if "updated_at" in attributes:
            self._updated_at = self._makeDatetimeAttribute(attributes["updated_at"])
        if "visibility" in attributes:
            self._visibility = self._makeStringAttribute(attributes["visibility"])
        if "selected_repositories_url" in attributes:
            self._selected_repositories_url = self._makeStringAttribute(attributes["selected_repositories_url"])
        if "url" in attributes:
            self._url = self._makeStringAttribute(attributes["url"])
