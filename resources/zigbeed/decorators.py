# This file is part of Jeedom.
#
# Jeedom is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Jeedom is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Jeedom. If not, see <http://www.gnu.org/licenses/>.

"""Decorators for ZHA core registries."""
from typing import Callable, TypeVar, Union

CALLABLE_T = TypeVar("CALLABLE_T", bound=Callable)  # pylint: disable=invalid-name

class DictRegistry(dict):
	"""Dict Registry of items."""

	def register(self, name: Union[int, str], item: Union[str, CALLABLE_T] = None) -> Callable[[CALLABLE_T], CALLABLE_T]:
		"""Return decorator to register item with a specific name."""

		def decorator(channel: CALLABLE_T) -> CALLABLE_T:
			"""Register decorated channel or item."""
			if item is None:
				self[name] = channel
			else:
				self[name] = item
			return channel
		return decorator

class SetRegistry(set):
	"""Set Registry of items."""

	def register(self, name: Union[int, str]) -> Callable[[CALLABLE_T], CALLABLE_T]:
		"""Return decorator to register item with a specific name."""

		def decorator(channel: CALLABLE_T) -> CALLABLE_T:
			"""Register decorated channel or item."""
			self.add(name)
			return channel
		return decorator
