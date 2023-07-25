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
from typing import Any

from github.GithubObject import NotSet, Opt
from github.PaginatedList import PaginatedList
from github.Repository import Repository
from github.Variable import Variable


class OrganizationVariable(Variable):
    """
    This class represents a org level GitHub variable. The reference can be found here https://docs.github.com/en/rest/actions/variables
    """

    @property
    def visibility(self) -> str:
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

    def edit(
        self,
        value: str,
        visibility: str = "all",
        selected_repositories: Opt[PaginatedList[Repository]] = NotSet,
    ) -> bool:
        """
        :calls: `PATCH /orgs/{org}/actions/variables/{variable_name} <https://docs.github.com/en/rest/reference/actions/variables#update-an-organization-variable>`_
        :param variable_name: string
        :param value: string
        :param visibility: string
        :param selected_repositories: Optional list of :class:`github.Repository.Repository`
        :rtype: bool
        """
        assert isinstance(value, str), value
        assert isinstance(visibility, str), visibility
        if visibility == "selected":
            assert isinstance(selected_repositories, PaginatedList) and all(
                isinstance(element, Repository) for element in selected_repositories
            ), selected_repositories
        else:
            assert selected_repositories is NotSet

        patch_parameters = {
            "name": self.name,
            "value": value,
            "visibility": visibility,
        }
        if selected_repositories is not NotSet:
            patch_parameters["selected_repository_ids"] = [element.id for element in selected_repositories]

        status, headers, data = self._requester.requestJson(
            "PATCH",
            f"{self.url}/actions/variables/{self.name}",
            input=patch_parameters,
        )
        return status == 204

    def add_repo(self, repo: Repository) -> bool:
        """
        :calls: 'PUT {org_url}/actions/variables/{secret_name} <https://docs.github.com/en/rest/actions/variables#add-selected-repository-to-an-organization-secret>`_
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
        :calls: 'DELETE {org_url}/actions/variables/{secret_name} <https://docs.github.com/en/rest/actions/variables#add-selected-repository-to-an-organization-secret>`_
        :param repo: github.Repository.Repository
        :rtype: bool
        """
        if self.visibility != "selected":
            return False
        self._requester.requestJsonAndCheck("DELETE", f"{self.url}/repositories/{repo.id}")
        self._selected_repositories.value.remove(repo)
        return True

    def _initAttributes(self) -> None:
        self._name = NotSet
        self._created_at = NotSet
        self._updated_at = NotSet
        self._visibility = NotSet
        self._selected_repositories = NotSet
        self._selected_repositories_url = NotSet
        self._url = NotSet

    def _useAttributes(self, attributes: dict[str, Any]) -> None:
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
