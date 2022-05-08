# OS6-memory-allocation-by-variable-size-partitions
##### In this project, I have implemented a simulation of memory allocation with variable size partitions.

The main and only class is Window, more about the fields and methods of this class.

Fields:
* `disk` - full memory
* `busy_mem` - busy memory
* `table` - memory simulation
Stored as a list of parcels
Each section is a list of three variables: whether the cell is empty, start index, size
* `queue` - queue simulation, stores the sizes of tasks in the queue
* `clean_app` `font` `enter_pressed` `enter_button_rect` `enter_rect` - font, pictures and rects for entering the task
* `is_writing` `text_written` - input variables: whether and what is entered
* `full_info` `switch_on `switch_rect` - variables for switching the output of full information
* `clean_task` `clean_queue` `task_button` `queue_button` `tasks_rect` `queue_rect` - pictures and rects for the main part
* `tasks_pos max_tasks_pos` - shift and maximum shift for running tasks (carried out by mouse wheel)
* `queue_pos max_queue_pos` - similar for queue
* `tasks_buttons_rects` - list of rectors for stop buttons for current tasks
* `queue_buttons_rects` - similar for queue

Methods:
* `check_queue(self)` - checks if something in the queue can start executing
* `add_task(self, size)` - finds a place in memory and sets the task for execution, otherwise queues it, takes the size of the task
* `check_table(self)` - checks the table for empty cells in a row, merges these cells
* `del_task(self, index)` - removes a task from being executed by its serial number in memory (counting from 0)
* `gen_work_surf(self)` - generates a surface with running tasks, keeps track of `tasks_pos`, comparing it with `max_tasks_pos`, returns the surface (often it can be y larger than the screen)
* `gen_queue_surf(self)` - same for queue
* `gen_info_surf(self)` - generates a surface with complete information
* `event_work(self, event)` - handles events like all similar methods in my project classes
* `update(self)` - collects the complete surface and draws it on the screen, also selects the necessary parts of the surfaces obtained from `gen_work_surf(self)` and `gen_queue_surf(self)`
