### Things to avoid. ###
- Don't mix bmesh and bpy.ops.mesh while working on the same mesh, that's a recipe for bad code and potential crashes.

    ```
    if chboxjoin0:
        # bpy.ops.mesh.vert_connect_path()
        bm.edges.new([v1, v2])
    ```

- BGL is one of the few areas in blender that will cause crashes to desktop, you must deal with all errors/exceptions inside your bgl callback, and return the bgl to a safe default state if there are errors.

- Don't mix geometry modifications inside your bgl callback

- Separate bgl parts from bmesh/mesh operations

- Perform mesh operations first, then draw the results.

- Switching contexts inside bgl callback, probably not a good idea.

- Start a lot simpler, maybe even with completely unrelated code just to get a better understanding of the interactions between various parts of your code.
