class AnsibleUtils:
    def __init__(self, ansible_inventory, ansible_playbook):
        self.ansible_inventory = ansible_inventory
        self.ansible_playbook = ansible_playbook

    def run_playbook(self, extra_vars=None):
        from ansible.playbook import Playbook
        from ansible.inventory.manager import InventoryManager
        from ansible.vars.manager import VariableManager
        from ansible.executor.playbook_executor import PlaybookExecutor

        inventory = InventoryManager(loader=None, sources=self.ansible_inventory)
        variable_manager = VariableManager(loader=None, inventory=inventory)

        playbook_executor = PlaybookExecutor(
            playbooks=[self.ansible_playbook],
            inventory=inventory,
            variable_manager=variable_manager,
            loader=None,
            passwords=None
        )

        if extra_vars:
            variable_manager.extra_vars = extra_vars

        results = playbook_executor.run()
        return results

    def execute_command(self, host, command):
        from ansible.module_utils.basic import AnsibleModule
        from ansible.executor.task_executor import TaskExecutor

        module_args = dict(command=command)
        module = AnsibleModule(argument_spec=module_args)

        task_executor = TaskExecutor(module, host)
        result = task_executor.run()
        return result